from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.database import init_db
from app.config import settings
from app.services.embeddings import init_qdrant
from app.utils.errors import APIError
import os

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Initialize database
init_db()

# Initialize Qdrant vector database
try:
    init_qdrant()
except Exception as e:
    print(f"Warning: Could not initialize Qdrant: {e}")

# Create app
app = FastAPI(
    title=settings.app_name,
    description="AI operations assistant for vacation rental property managers",
    version="0.1.0",
)

# CORS
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """Handle APIError exceptions with standardized response format."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with generic error response."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "code": "INTERNAL_ERROR",
        },
    )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "iTrip AI Command Center API",
        "version": "0.1.0",
        "ai_provider": settings.ai_provider,
        "database": settings.database_url,
    }


@app.get("/health")
async def health():
    """Health check for deployment."""
    return {"status": "ok"}


# Import routers
from app.routers import auth, documents, property_brain, guest_reply, revenue_analysis
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(property_brain.router)
app.include_router(guest_reply.router)
app.include_router(revenue_analysis.router)

# Coming next
# from app.routers import revenue, quotes
# app.include_router(revenue.router)
# app.include_router(quotes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
