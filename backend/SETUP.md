# Backend Setup & Testing

## Prerequisites
- Python 3.10+
- pip package manager

## Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your chosen API key (Gemini, OpenAI, or Anthropic).

5. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Server will be available at `http://localhost:8000`

## API Documentation

Once running, view interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing Authentication Endpoints

### Using curl or Postman

**1. Register a new user**:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d {
    "email": "staff@itrip.com",
    "password": "SecurePassword123",
    "full_name": "John Doe"
  }
```

**2. Login**:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d {
    "email": "staff@itrip.com",
    "password": "SecurePassword123"
  }
```

Response will include:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**3. Use token in requests**:
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**4. Logout**:
```bash
curl -X POST "http://localhost:8000/auth/logout"
```

## Database

SQLite database will be created at `data/app.db` on first run. 

To reset database, delete the `data/` folder and restart the server.

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Settings from .env
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── database.py       # Database setup
│   ├── routers/
│   │   ├── auth.py       # Authentication endpoints
│   │   └── ...           # Other modules (coming soon)
│   ├── services/
│   │   ├── auth_service.py  # Password & JWT utilities
│   │   └── ...              # Other services (coming soon)
│   └── middleware/
│       └── auth.py       # JWT token validation
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
└── SETUP.md             # This file
```

## Next Steps

1. Test auth endpoints using Swagger UI at http://localhost:8000/docs
2. Once working, build Phase 2: File Ingestion Pipeline
