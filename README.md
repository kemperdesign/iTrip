# iTrip AI Command Center

An AI-powered operations assistant for vacation rental property managers. Helps staff answer guest questions, analyze revenue, and build pricing quotes using their property documents and historical data.

## Features (MVP)

- **Property Brain**: Q&A over property documents and notes
- **Guest Reply Assistant**: Draft responses to guest inquiries
- **Revenue Analyst**: Analyze historical performance and trends
- **Quote Builder**: Generate pricing recommendations based on historical data
- **File Uploads**: Support DOCX, XLSX, and PDF uploads
- **Multi-AI Support**: Works with Gemini, OpenAI, or Anthropic APIs

## Project Structure

```
.
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── routers/
│   └── requirements.txt
├── frontend/         # Next.js React frontend
│   ├── src/
│   │   └── app/
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (for Qdrant vector database)
- API key from Gemini, OpenAI, or Anthropic

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API key

# Run development server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 3. Vector Database (Optional for MVP)

```bash
docker-compose up
```

This starts PostgreSQL and Qdrant (when needed in Phase 2).

## Configuration

Create a `.env` file in the `backend/` directory:

```env
AI_PROVIDER="gemini"  # or "openai" or "anthropic"
GEMINI_API_KEY="your-api-key"
DATABASE_URL="sqlite:///./data/app.db"
SECRET_KEY="your-secret-key"
```

## Development

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run type-check
```

### Building for Production

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm run build
npm start
```

## Implementation Phases

1. ✅ **Phase 1**: Project setup & foundation
2. 🔄 **Phase 2**: File ingestion pipeline
3. 📋 **Phase 3**: Property Brain module
4. 📋 **Phase 4**: Guest Reply Assistant
5. 📋 **Phase 5**: Revenue Analyst module
6. 📋 **Phase 6**: Quote Builder module
7. 📋 **Phase 7**: Polish & documentation

## API Endpoints (Coming Soon)

### Authentication
- `POST /auth/login` - Staff login
- `POST /auth/logout` - Logout

### Documents
- `POST /documents/upload` - Upload property docs/data
- `GET /documents` - List uploaded documents

### Property Brain
- `POST /property-brain/ask` - Ask questions about properties

### Guest Replies
- `POST /guest-reply/generate` - Draft guest responses

### Revenue Analysis
- `GET /revenue/summary` - Get revenue insights
- `GET /revenue/top-properties` - Top performing properties

### Quote Builder
- `POST /quotes/recommend` - Get quote recommendations

## Data Files

The MVP uses these data sources:
- `example of internal property data.docx` - Property information and check-in instructions
- `NEW common responses doc.docx` - Guest response templates
- `Copy of Historical data 2025.xlsx` - Revenue, ADR, and occupancy data

Place these in the `data/` folder and upload via the app.

## License

Proprietary - iTrip Vacations

## Support

For questions or issues, contact the development team.
