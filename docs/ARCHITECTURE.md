# Architecture Overview

Complete technical architecture and system design for iTrip.

## Table of Contents

- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Module Design](#module-design)
- [Database Schema](#database-schema)
- [Multi-Provider AI Abstraction](#multi-provider-ai-abstraction)
- [Authentication & Security](#authentication--security)
- [Deployment Architecture](#deployment-architecture)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Next.js Frontend (React 18 + TypeScript + Tailwind CSS)  │   │
│  │  • Components (Quote Builder, Revenue Analysis, etc.)    │   │
│  │  • State Management (React Hooks)                        │   │
│  │  • Error Boundaries & Toast Notifications               │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────┘
                                 │ HTTP/REST
                                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  FastAPI Backend (Python 3.10+ with Pydantic)            │   │
│  │  • routers/ - API endpoints                             │   │
│  │  • services/ - Business logic                           │   │
│  │  • middleware/ - Authentication & logging               │   │
│  │  • models/ - ORM definitions                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ↓            ↓            ↓
      ┌──────────────────┐ ┌──────────┐ ┌──────────────┐
      │  DATA LAYER      │ │VECTOR DB │ │  AI PROVIDERS│
      │                  │ │          │ │              │
      │ SQLite/Postgres  │ │ Qdrant   │ │ OpenAI       │
      │ • Properties     │ │ Vector   │ │ Anthropic    │
      │ • Users          │ │ Search   │ │ Google       │
      │ • Documents      │ │ (Semantic│ │ (Multi-API)  │
      │ • Revenue Data   │ │ Search)  │ │              │
      │ • Quotes         │ │          │ │              │
      └──────────────────┘ └──────────┘ └──────────────┘
```

### Component Layers

```
┌─ PRESENTATION LAYER ─────────────────────────────────────────┐
│  • React Components (Sidebar, Quote Builder, etc.)           │
│  • Page routing via Next.js                                   │
│  • Toast notifications & error boundaries                    │
│  • Form validation & user feedback                           │
└───────────────────────────────────────────────────────────────┘
         ↑                                              ↓
┌─ API/INTEGRATION LAYER ──────────────────────────────────────┐
│  • FastAPI routes (/property-brain, /quotes, etc.)           │
│  • Request validation (Pydantic)                             │
│  • Response serialization                                     │
│  • JWT authentication middleware                              │
└───────────────────────────────────────────────────────────────┘
         ↑                                              ↓
┌─ BUSINESS LOGIC LAYER ───────────────────────────────────────┐
│  • Services:                                                  │
│    - property_brain_service (Q&A)                            │
│    - guest_reply_service (Reply generation)                 │
│    - revenue_analysis_service (Analytics)                   │
│    - pricing_service (Quote calculation)                    │
│    - file_processor (Document parsing)                      │
│    - embeddings (Vector search)                             │
└───────────────────────────────────────────────────────────────┘
         ↑                                              ↓
┌─ DATA ACCESS LAYER ──────────────────────────────────────────┐
│  • SQLAlchemy ORM models                                     │
│  • Database queries & transactions                            │
│  • Vector database queries (Qdrant)                          │
│  • External API calls (AI providers)                         │
└───────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | Next.js | 14+ | Server-side rendering & routing |
| Language | TypeScript | 5.0+ | Type safety |
| UI Framework | React | 18+ | Component library |
| Styling | Tailwind CSS | 3.3+ | Utility-first CSS |
| Components | shadcn/ui | Latest | Pre-built UI components |
| HTTP Client | Fetch API | - | API communication |
| State | React Hooks | 18+ | State management |
| Form Validation | Client-side | - | Input validation |

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | FastAPI | 0.95+ | Web framework |
| Language | Python | 3.10+ | Backend language |
| ORM | SQLAlchemy | 2.0+ | Database abstraction |
| Validation | Pydantic | 2.0+ | Data validation |
| Authentication | JWT | - | Token-based auth |
| Async | asyncio | - | Asynchronous operations |
| File Processing | python-docx, openpyxl, pypdf | Latest | Document parsing |

### Database

| Component | Technology | Env | Purpose |
|-----------|-----------|-----|---------|
| Relational DB | SQLite | Dev | Application data |
| Relational DB | PostgreSQL | Prod | Scalable storage |
| Vector DB | Qdrant | Dev/Prod | Semantic search |
| Embeddings | OpenAI API | - | Text vectorization |

### AI/ML

| Component | Provider | Models | Purpose |
|-----------|----------|--------|---------|
| Large Language | OpenAI | GPT-4, GPT-3.5 | AI reasoning |
| Large Language | Anthropic | Claude Opus, Sonnet, Haiku | AI reasoning |
| Large Language | Google | Gemini 2.0, 1.5 | AI reasoning |
| Embeddings | OpenAI | text-embedding-3-small | Vector search |

### DevOps

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Containerization | Docker | Application containers |
| Orchestration | Docker Compose | Local development |
| CI/CD | GitHub Actions | Testing & deployment |
| Version Control | Git | Source code management |

---

## Data Flow

### Quote Generation Flow

```
User Input
├─ Property ID, dates, guests
└─ Guest type, season flags
    ↓
[Quote Builder Form]
    ↓
[POST /revenue-analysis/quotes/generate]
    ↓
[Backend Routing]
    ↓
[pricing_service.generate_advanced_quote()]
    ├─ Query RevenueData for comparable dates
    ├─ Calculate seasonal_multiplier
    ├─ Calculate guest_type_factor
    ├─ Calculate length_of_stay_factor
    ├─ Apply all multipliers to base ADR
    ├─ Calculate fees (cleaning, service, tax)
    ├─ Generate three-tier rates (conservative, recommended, aggressive)
    └─ Call AI provider for pricing reasoning
        ├─ OpenAI (gpt-3.5-turbo/gpt-4)
        ├─ Anthropic (Claude)
        └─ Gemini (Google)
    ↓
[Save QuoteRecommendation to database]
    ↓
[Response with quote details]
    ↓
[Frontend displays three-tier pricing]
```

### Property Brain Q&A Flow

```
User Question
├─ "What is the WiFi password?"
└─ Question text
    ↓
[Property Brain Page]
    ↓
[POST /property-brain/ask]
    ↓
[Backend Routing]
    ↓
[property_brain_service.generate_answer()]
    ├─ Generate embedding for question
    │  └─ Call OpenAI text-embedding-3-small API
    ├─ Search similar document chunks in Qdrant
    │  └─ Semantic similarity search
    ├─ Retrieve top-K relevant chunks
    └─ Generate answer via AI provider
        ├─ System prompt: "You are a helpful assistant answering about properties"
        ├─ Context: Retrieved document chunks
        ├─ User prompt: Original question
        └─ AI provider (OpenAI/Anthropic/Gemini)
    ↓
[Return answer + source references]
    ↓
[Frontend displays answer with source documents]
```

### Guest Reply Generation Flow

```
Guest Message
├─ Incoming email from guest
└─ "The bed is broken and I want a refund"
    ↓
[Guest Reply Page]
    ↓
[POST /guest-replies/generate]
    ↓
[Backend Routing]
    ↓
[guest_reply_service.generate_guest_reply()]
    ├─ Detect escalation risks
    │  ├─ Check for refund/damage/complaint keywords
    │  └─ Classify risk level (low/medium/high/escalate)
    ├─ Search response templates via embeddings
    │  ├─ Generate message embedding
    │  ├─ Query Qdrant for similar template chunks
    │  └─ Retrieve top templates as context
    └─ Generate reply via AI provider
        ├─ System prompt: "Draft professional guest reply"
        ├─ Context: Response templates + detected risks
        ├─ User prompt: Original guest message
        └─ AI provider
    ↓
[Return reply + risk flags + templates]
    ↓
[Frontend displays reply for approval]
    ↓
[Staff reviews and approves]
    ↓
[Reply saved to database with approval status]
```

### Document Upload & Indexing Flow

```
File Upload
├─ DOCX, XLSX, or PDF
└─ Via /documents/upload
    ↓
[File Validation]
├─ Check file type
├─ Check file size
└─ Scan for malicious content
    ↓
[Parse Document]
├─ DOCX: python-docx → extract text, tables
├─ XLSX: openpyxl → extract cells, values
└─ PDF: pypdf → extract text per page
    ↓
[Chunk Text]
├─ Split into ~300-500 character chunks
└─ Maintain context (overlap ~50 chars)
    ↓
[Generate Embeddings]
└─ OpenAI text-embedding-3-small API
    ├─ Batch process all chunks
    └─ Get 1536-dim vector per chunk
    ↓
[Store in Vector Database]
└─ Qdrant
    ├─ Store embeddings
    ├─ Store chunk text
    └─ Store document metadata
    ↓
[Store in Relational Database]
└─ SQLite/PostgreSQL
    ├─ Document record
    ├─ Document metadata
    └─ Chunks count
    ↓
[Update UI with status]
└─ Frontend polls /documents for status
```

---

## Module Design

### Property Brain Module

**Responsibility**: Semantic Q&A over documents

**Components:**
- `property_brain_service.py`: Core logic
  - `generate_answer()`: Main entry point
  - `search_similar()`: Query Qdrant
  - `_get_ai_response()`: Multi-provider abstraction
- `property_brain.py`: Router
  - `POST /property-brain/ask`: API endpoint
- `embeddings.py`: Vector operations
  - `create_embeddings()`: Generate vectors
  - `search_similar()`: Semantic search

**Data Flow:**
1. User submits question
2. Service generates embedding for question
3. Service queries Qdrant for similar document chunks
4. Service builds context from retrieved chunks
5. Service calls AI provider with question + context
6. Response returned with source references

### Guest Reply Module

**Responsibility**: Draft replies to guest messages

**Components:**
- `guest_reply_service.py`: Core logic
  - `generate_guest_reply()`: Main entry point
  - `detect_escalation_risks()`: Risk detection
  - `_get_ai_response()`: Multi-provider abstraction
- `guest_reply.py`: Router
  - `POST /guest-replies/generate`: Generate reply
  - `POST /guest-replies/{id}/approve`: Approve reply
- `schemas.py`: Data models
  - `GenerateGuestReplyRequest`
  - `GenerateGuestReplyResponse`
  - `RiskFlag`

**Escalation Risk Keywords:**
```python
{
  "refund": "high",
  "damage": "high",
  "complaint": "medium",
  "cancel": "medium",
  "broken": "high",
  ...
}
```

### Revenue Analysis Module

**Responsibility**: Analytics and pricing insights

**Components:**
- `revenue_analysis_service.py`: Core logic
  - `analyze_revenue()`: Comprehensive analysis
  - `get_top_properties()`: Ranking
  - `get_property_trends()`: Trend analysis
  - `generate_quote()`: Quote generation
- `pricing_service.py`: Pricing calculations
  - `calculate_seasonal_multiplier()`
  - `calculate_guest_type_factor()`
  - `calculate_length_of_stay_factor()`
  - `calculate_fees()`
  - `generate_advanced_quote()`
- `revenue_analysis.py`: Routers
  - `POST /revenue-analysis/analyze`
  - `GET /revenue-analysis/top-properties`
  - `GET /revenue-analysis/property/{id}/trends`
  - `POST /revenue-analysis/quotes/generate`

**Pricing Multipliers:**
```
Seasonal: 0.7 - 1.3 (off-season to peak)
Guest Type: 0.9 - 1.1 (group to family)
Stay Length: 0.8 - 1.05 (monthly to weekend)
```

---

## Database Schema

### Core Tables

```sql
-- Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    is_active BOOLEAN,
    is_superuser BOOLEAN,
    created_at TIMESTAMP
);

-- Properties
CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    address VARCHAR,
    base_adr FLOAT,
    description TEXT,
    created_at TIMESTAMP
);

-- Documents
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    filename VARCHAR,
    document_type VARCHAR,
    file_size_bytes INTEGER,
    pages INTEGER,
    chunks_count INTEGER,
    embedding_status VARCHAR,
    uploaded_at TIMESTAMP,
    uploaded_by_id INTEGER,
    FOREIGN KEY (uploaded_by_id) REFERENCES users(id)
);

-- Document Chunks
CREATE TABLE document_chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER,
    chunk_index INTEGER,
    text TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

-- Revenue Data
CREATE TABLE revenue_data (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    date DATE,
    revenue FLOAT,
    adr FLOAT,
    occupancy_rate FLOAT,
    bookings INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties(id)
);

-- Quote Recommendations
CREATE TABLE quote_recommendations (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,
    arrival_date DATE,
    departure_date DATE,
    nights INTEGER,
    guest_count INTEGER,
    guest_type VARCHAR,
    base_adr FLOAT,
    seasonal_multiplier FLOAT,
    guest_type_factor FLOAT,
    length_of_stay_factor FLOAT,
    base_rate FLOAT,
    cleaning_fee FLOAT,
    service_fee FLOAT,
    pet_fee FLOAT,
    taxes FLOAT,
    conservative_rate FLOAT,
    conservative_total FLOAT,
    recommended_rate FLOAT,
    recommended_total FLOAT,
    aggressive_rate FLOAT,
    aggressive_total FLOAT,
    staff_override_rate FLOAT,
    staff_notes TEXT,
    status VARCHAR,
    created_at TIMESTAMP,
    created_by_id INTEGER,
    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (created_by_id) REFERENCES users(id)
);

-- AI Responses
CREATE TABLE ai_responses (
    id INTEGER PRIMARY KEY,
    response_type VARCHAR,
    model_type VARCHAR,
    content TEXT,
    tokens_used INTEGER,
    cost FLOAT,
    ai_provider VARCHAR,
    approved_by_id INTEGER,
    response_status VARCHAR,
    created_at TIMESTAMP,
    FOREIGN KEY (approved_by_id) REFERENCES users(id)
);
```

### Qdrant Collections

**Collection: `itrip_documents`**
- Vector size: 1536 (OpenAI text-embedding-3-small)
- Points: Document chunks
- Payload:
  ```json
  {
    "document_id": 1,
    "filename": "property-info.docx",
    "chunk_index": 0,
    "text": "WiFi Network...",
    "document_type": "property_document"
  }
  ```

---

## Multi-Provider AI Abstraction

### Architecture

```python
# Service pattern - single interface, multiple providers

def _get_ai_response(system_prompt, user_prompt, ai_provider=None):
    """Route to appropriate provider based on config"""
    provider = ai_provider or settings.AI_PROVIDER
    
    if provider == "openai":
        return _openai_response(system_prompt, user_prompt)
    elif provider == "anthropic":
        return _anthropic_response(system_prompt, user_prompt)
    elif provider == "gemini":
        return _gemini_response(system_prompt, user_prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")
```

### Provider Implementations

**OpenAI:**
```python
def _openai_response(system_prompt, user_prompt):
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=settings.ai_model or "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content
```

**Anthropic:**
```python
def _anthropic_response(system_prompt, user_prompt):
    client = Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model=settings.ai_model or "claude-opus-4-7",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response.content[0].text
```

**Gemini:**
```python
def _gemini_response(system_prompt, user_prompt):
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(
        model_name=settings.ai_model or "gemini-2.0-flash",
        system_instruction=system_prompt
    )
    response = model.generate_content(user_prompt)
    return response.text
```

### Model Selection

| Provider | Model | Capability | Cost |
|----------|-------|-----------|------|
| OpenAI | gpt-4 | Highest | $$$ |
| OpenAI | gpt-3.5-turbo | Good | $ |
| Anthropic | claude-opus-4-7 | Highest | $$$ |
| Anthropic | claude-sonnet-4-6 | Good | $$ |
| Google | gemini-2.0-flash | Good | $ |
| Google | gemini-1.5-pro | Highest | $$ |

---

## Authentication & Security

### JWT Authentication Flow

```
1. User submits credentials (email + password)
   ↓
2. Backend verifies password hash
   ↓
3. Backend generates JWT token
   ├─ Payload: user_id, email, exp (24 hours)
   ├─ Algorithm: HS256
   └─ Secret key: settings.SECRET_KEY
   ↓
4. Token sent to frontend
   ↓
5. Frontend stores token in httpOnly cookie
   ↓
6. Subsequent requests include token in header:
   Authorization: Bearer <token>
   ↓
7. Backend middleware validates token signature
   ↓
8. Request proceeds with authenticated user
```

### Middleware

**auth.py**:
```python
async def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Validate JWT token and return user"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
```

### Security Best Practices

✅ **Implemented**:
- JWT tokens with expiration (24 hours)
- Password hashing with bcrypt
- httpOnly cookies (prevents XSS)
- Secure headers (CORS, CSP, etc.)
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- HTTPS-ready (production deployment)

🔒 **Configuration**:
```env
SECRET_KEY=<random-32-chars>        # Generate with secrets module
ALGORITHM=HS256                      # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=1440     # 24 hours
```

---

## Deployment Architecture

### Development

```
Laptop/Desktop
├── Frontend (npm run dev on port 3000)
├── Backend (uvicorn on port 8000)
├── SQLite database
└── Docker Qdrant (port 6333)
```

### Production

```
Cloud Server / On-Premise
├── Docker Container: iTrip Backend
│   ├── FastAPI on port 8000
│   ├── PostgreSQL connection
│   └── Environment variables
├── Docker Container: iTrip Frontend
│   ├── Next.js on port 3000
│   └── Environment configuration
├── PostgreSQL Database (RDS or local)
├── Qdrant Vector Database
├── S3/Blob Storage (for file uploads)
└── Load Balancer (Nginx)
```

### Scaling Considerations

**Horizontal Scaling**:
- Run multiple backend instances behind load balancer
- Cache layer for frequently accessed data (Redis)
- Database read replicas for heavy queries

**Performance Optimization**:
- API response caching (Redis)
- Document chunk caching for popular files
- Batch embeddings generation
- Connection pooling (PostgreSQL)

---

## API Contract Design

### Request/Response Pattern

**Request:**
```json
{
  "property_id": 1,
  "arrival_date": "2024-06-15",
  "departure_date": "2024-06-22"
}
```

**Response (Success):**
```json
{
  "quote_id": 42,
  "property_id": 1,
  "recommended_rate": 198.00,
  "status": "success"
}
```

**Response (Error):**
```json
{
  "detail": "Property not found",
  "code": "NOT_FOUND",
  "status_code": 404
}
```

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Quote generated successfully |
| 201 | Created | Document uploaded |
| 400 | Bad Request | Invalid date range |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | User doesn't own property |
| 404 | Not Found | Property doesn't exist |
| 422 | Validation Error | Invalid guest count |
| 429 | Rate Limited | Too many requests |
| 500 | Server Error | Unexpected error |

---

For implementation details, see [DEVELOPMENT.md](../DEVELOPMENT.md) and [API.md](./API.md).
