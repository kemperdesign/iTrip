from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
import logging
from app.database import get_db
from app.models import User, Document
from app.middleware.auth import get_current_active_user
from app.services.property_brain_service import query_property_brain
from pydantic import BaseModel
from app.utils.errors import ValidationError, NotFoundError, InternalServerError, log_error

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/property-brain", tags=["property_brain"])


class PropertyBrainQuery(BaseModel):
    question: str
    document_id: Optional[int] = None
    top_k: int = 5


class PropertyBrainResponse(BaseModel):
    answer: str
    sources: list
    provider: str


@router.post("/ask", response_model=PropertyBrainResponse)
async def ask_property_brain(
    query: PropertyBrainQuery,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Ask a question about property information using semantic search."""
    try:
        if not query.question or len(query.question.strip()) < 1:
            raise ValidationError("Question cannot be empty")

        if query.document_id:
            doc = db.query(Document).filter(Document.id == query.document_id).first()
            if not doc:
                raise NotFoundError("Document", query.document_id)

        if query.top_k < 1 or query.top_k > 20:
            raise ValidationError("top_k must be between 1 and 20")

        result = query_property_brain(
            question=query.question,
            document_id=query.document_id,
            top_k=query.top_k,
        )
        return result
    except (ValidationError, NotFoundError):
        raise
    except Exception as e:
        log_error("ask_property_brain", e)
        raise InternalServerError(f"Failed to process query: {str(e)}")
