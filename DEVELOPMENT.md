# Development Guide

Complete guide for setting up and developing iTrip locally.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Backend Development](#backend-development)
4. [Frontend Development](#frontend-development)
5. [Database & Vector Search](#database--vector-search)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Troubleshooting](#troubleshooting)
9. [Deployment](#deployment)

---

## Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **Git** — [Download](https://git-scm.com/)
- **Docker & Docker Compose** (optional, for Qdrant/PostgreSQL)
- **VS Code** (recommended IDE)

### Recommended VS Code Extensions

```
- Python
- Pylance
- FastAPI
- ES7+ React/Redux/React-Native snippets
- ESLint
- Prettier
- TypeScript Vue Plugin (Volar)
```

---

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kemperdesign/iTrip.git
cd iTrip
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 3. Configure Environment (.env)

Edit `backend/.env`:

```env
# AI Provider Configuration
AI_PROVIDER=openai  # openai, anthropic, or gemini
OPENAI_API_KEY=sk-...
# OR
# ANTHROPIC_API_KEY=sk-ant-...
# OR
# GEMINI_API_KEY=...

# Database
DATABASE_URL=sqlite:///./itrip.db

# JWT Secret (generate: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=your-super-secret-key-here

# Vector Search (if using Qdrant)
QDRANT_URL=http://localhost:6333

# Server
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file (optional, usually uses API_URL from environment)
# .env.local for local overrides
```

### 5. Optional: Set Up Docker Services

```bash
# From project root
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Qdrant vector database (port 6333)

---

## Backend Development

### Running the Backend

```bash
cd backend
source venv/bin/activate  # Activate venv
uvicorn app.main:app --reload --port 8000
```

**API will be available at http://localhost:8000**
**API documentation: http://localhost:8000/docs**

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Settings and environment
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # ORM models
│   ├── schemas.py           # Pydantic schemas
│   ├── middleware/
│   │   └── auth.py          # JWT validation
│   ├── routers/
│   │   ├── auth.py          # Login/logout
│   │   ├── documents.py     # File upload/management
│   │   ├── property_brain.py
│   │   ├── guest_reply.py
│   │   └── revenue_analysis.py
│   └── services/
│       ├── file_processor.py
│       ├── embeddings.py
│       ├── property_brain_service.py
│       ├── guest_reply_service.py
│       ├── revenue_analysis_service.py
│       └── pricing_service.py
├── requirements.txt
└── .env
```

### Database Initialization

The SQLite database is created automatically on first run. To reset:

```bash
# Windows
del itrip.db

# Mac/Linux
rm itrip.db

# Restart the server
uvicorn app.main:app --reload
```

### Making API Requests

Use the interactive docs at http://localhost:8000/docs to test endpoints.

Or use curl/httpie:

```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Ask Property Brain
curl -X POST "http://localhost:8000/property-brain/ask" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the wifi password?"}'
```

### Adding New Endpoints

1. Create a new file in `app/routers/` (e.g., `new_router.py`)
2. Import it in `app/main.py`
3. Register it: `app.include_router(new_router.router)`

Example router:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/api/resource", tags=["resource"])

@router.get("/")
async def get_resources(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all resources."""
    return {"resources": []}
```

---

## Frontend Development

### Running the Frontend

```bash
cd frontend
npm run dev
```

**Frontend will be available at http://localhost:3000**

### Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home page
│   │   ├── quote-builder/
│   │   ├── quotes/
│   │   ├── property-brain/
│   │   ├── guest-reply/
│   │   ├── revenue-analysis/
│   │   ├── imports/
│   │   └── globals.css
│   ├── components/
│   │   ├── layout/
│   │   ├── modules/
│   │   ├── common/
│   │   └── ErrorBoundary.tsx
│   ├── hooks/
│   │   └── useToast.ts
│   └── services/
│       └── api.ts
├── package.json
├── tsconfig.json
├── next.config.js
└── tailwind.config.js
```

### Available npm Scripts

```bash
npm run dev          # Start development server
npm run build        # Build production bundle
npm run start        # Run production build
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run type-check   # Check TypeScript types
npm test             # Run unit tests
```

### Adding New Pages

1. Create directory in `src/app/` (e.g., `src/app/new-feature/`)
2. Create `page.tsx` in that directory
3. The route is automatically created: `/new-feature`

Example page:

```typescript
// src/app/new-feature/page.tsx
"use client";

import { useEffect, useState } from "react";

export default function NewFeature() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold">New Feature</h1>
    </div>
  );
}
```

### Using the Toast System

```typescript
import { useToast } from "@/hooks/useToast";

export function MyComponent() {
  const { success, error, warning } = useToast();

  async function handleAction() {
    try {
      await someAction();
      success("Action completed!");
    } catch (err) {
      error("Something went wrong");
    }
  }

  return <button onClick={handleAction}>Click me</button>;
}
```

---

## Database & Vector Search

### SQLite (Default)

Database file: `backend/itrip.db`

Reset database:
```bash
rm backend/itrip.db
```

### PostgreSQL (Production)

To use PostgreSQL instead:

```bash
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/itrip

# Start PostgreSQL container
docker-compose up -d postgres

# Create database
createdb -h localhost -U postgres itrip
```

### Qdrant (Vector Search)

```bash
# Start Qdrant
docker-compose up -d qdrant

# Access Qdrant admin UI at http://localhost:6333/dashboard
```

Qdrant stores document embeddings for semantic search. Collections are created automatically when documents are uploaded.

---

## Testing

### Backend Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_pricing.py -v

# Run specific test
pytest tests/test_pricing.py::test_seasonal_multiplier -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test QuoteBuilder.test.tsx
```

### E2E Testing (Manual)

1. Start all services (backend, frontend, docker)
2. Open http://localhost:3000
3. Login with `test@example.com` / `password`
4. Test key workflows:
   - Upload files
   - Ask Property Brain questions
   - Generate quotes
   - View quote history

---

## Debugging

### Backend Debugging with VS Code

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend",
      "env": {"PYTHONPATH": "${workspaceFolder}/backend"}
    }
  ]
}
```

### Frontend Debugging

1. Open Chrome DevTools: F12
2. Use Console, Network, and React DevTools tabs
3. Set breakpoints in Sources tab

### Viewing Logs

Backend logs appear in terminal. To save logs:

```bash
uvicorn app.main:app --reload > backend.log 2>&1
```

---

## Troubleshooting

### Common Issues

**ModuleNotFoundError in Python**
```bash
# Ensure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**npm dependencies issues**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port already in use**
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

**Database locked**
```bash
# Delete database and restart
rm backend/itrip.db
```

**Qdrant connection refused**
```bash
# Make sure Docker services are running
docker-compose up -d

# Check if Qdrant is running
curl http://localhost:6333/health
```

**Token expired**
- Frontend will redirect to login page
- Token lifetime is set in backend config (default: 24 hours)
- Create new token by logging in again

### Getting Help

1. Check [README.md](./README.md) for quick answers
2. Review error message carefully (often has the solution)
3. Check existing [GitHub Issues](https://github.com/kemperdesign/iTrip/issues)
4. Create new issue with:
   - Description of problem
   - Steps to reproduce
   - Error message/logs
   - Environment (OS, Python version, Node version)

---

## Deployment

### Local Production Build

```bash
# Build frontend
cd frontend
npm run build

# Install production dependencies
pip install -r requirements.txt
pip install gunicorn

# Run backend
cd backend
gunicorn app.main:app -w 4 -b 0.0.0.0:8000

# Serve frontend from .next/standalone
```

### Docker Deployment

```bash
# Build images
docker build -t itrip-backend ./backend
docker build -t itrip-frontend ./frontend

# Run containers
docker run -p 8000:8000 itrip-backend
docker run -p 3000:3000 itrip-frontend
```

### Environment Variables for Production

```env
# Production settings
DEBUG=false
ENVIRONMENT=production

# Strong secret key (generate: python -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=your-very-long-random-secret-key

# Database (use PostgreSQL in production)
DATABASE_URL=postgresql://user:password@db-host/itrip

# AI Provider
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...

# CORS
BACKEND_URL=https://your-domain.com
FRONTEND_URL=https://your-domain.com

# Email (if needed)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## Performance Tips

- Use Chrome DevTools Lighthouse for frontend performance
- Profile Python with `cProfile`: `python -m cProfile -s cumtime app.main`
- Monitor database queries: enable SQLAlchemy logging
- Cache expensive API calls where possible
- Use pagination for large data sets

---

For more details, see the [API documentation](./docs/API.md) and [feature guides](./docs/FEATURES.md).
