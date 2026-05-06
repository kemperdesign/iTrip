# API Reference

Complete API documentation for iTrip Backend. All endpoints are available at `http://localhost:8000` in development.

## Table of Contents

- [Authentication](#authentication)
- [Document Management](#document-management)
- [Property Brain](#property-brain)
- [Guest Reply Assistant](#guest-reply-assistant)
- [Revenue Analysis](#revenue-analysis)
- [Quote Builder](#quote-builder)
- [Error Handling](#error-handling)

---

## Authentication

### Login

**Endpoint:** `POST /auth/login`

Authenticate with email and password to receive JWT token.

**Request:**
```json
{
  "email": "test@example.com",
  "password": "password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "test@example.com",
    "is_active": true,
    "is_superuser": false
  }
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password"
  }'
```

### Logout

**Endpoint:** `POST /auth/logout`

Invalidate current session.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

## Document Management

### Upload Document

**Endpoint:** `POST /documents/upload`

Upload DOCX, XLSX, or PDF files for indexing and semantic search.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Parameters:**
- `file`: File to upload (multipart form data)
- `document_type`: Optional, defaults to "general"

**Response (200 OK):**
```json
{
  "id": 1,
  "filename": "property-info.docx",
  "document_type": "property_document",
  "size_bytes": 12345,
  "pages": 2,
  "chunks_count": 5,
  "embedding_status": "processing",
  "uploaded_at": "2024-05-06T10:00:00Z"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Authorization: Bearer <token>" \
  -F "file=@property-info.docx" \
  -F "document_type=property_document"
```

### List Documents

**Endpoint:** `GET /documents`

Retrieve all uploaded documents.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: Offset (default: 0)
- `limit`: Max results (default: 50)
- `document_type`: Filter by type (optional)

**Response (200 OK):**
```json
{
  "documents": [
    {
      "id": 1,
      "filename": "property-info.docx",
      "document_type": "property_document",
      "size_bytes": 12345,
      "pages": 2,
      "chunks_count": 5,
      "embedding_status": "complete",
      "uploaded_at": "2024-05-06T10:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 50
}
```

### Delete Document

**Endpoint:** `DELETE /documents/{document_id}`

Remove document and associated embeddings.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Document deleted successfully"
}
```

---

## Property Brain

### Ask Question

**Endpoint:** `POST /property-brain/ask`

Ask questions about property documents. Returns AI-generated answers with source references.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "question": "What is the Wi-Fi password?",
  "ai_provider": "openai"
}
```

**Response (200 OK):**
```json
{
  "question": "What is the Wi-Fi password?",
  "answer": "The Wi-Fi password is 'GuestPassword123'. The network name is 'PropertyGuests'.",
  "sources": [
    {
      "document_id": 1,
      "filename": "property-info.docx",
      "chunk": "WiFi Network: PropertyGuests\nPassword: GuestPassword123",
      "confidence": 0.95
    }
  ],
  "ai_provider": "openai",
  "ai_model": "gpt-3.5-turbo",
  "processing_time_ms": 1234
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/property-brain/ask" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What amenities are available?"
  }'
```

---

## Guest Reply Assistant

### Generate Reply

**Endpoint:** `POST /guest-replies/generate`

Generate AI-drafted replies to guest messages with escalation risk detection.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "message_id": 1,
  "ai_provider": "openai",
  "include_templates": true
}
```

**Response (200 OK):**
```json
{
  "ai_response_id": 5,
  "reply_text": "Thank you for reaching out! We're sorry to hear about the issue with the bed. We'll make this right for you. Please let us know the best way to contact you, and we'll arrange a replacement immediately.",
  "risk_flags": [
    {
      "keyword": "bed",
      "risk_level": "medium",
      "message_excerpt": "This bed is broken"
    }
  ],
  "source_templates": [
    {
      "document_id": 2,
      "filename": "guest-responses.docx",
      "chunk": "Thank you for reaching out. We'll resolve this quickly.",
      "confidence": 0.82
    }
  ],
  "ai_provider": "openai",
  "ai_model": "gpt-3.5-turbo",
  "requires_review": true
}
```

### Approve Reply

**Endpoint:** `POST /guest-replies/{ai_response_id}/approve`

Mark an AI-generated reply as approved and ready to send.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Reply approved",
  "ai_response_id": 5,
  "status": "approved"
}
```

---

## Revenue Analysis

### Analyze Revenue

**Endpoint:** `POST /revenue-analysis/analyze`

Get comprehensive revenue analysis with AI insights.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "property_id": 1,
  "start_date": "2024-01-01",
  "end_date": "2024-05-06"
}
```

**Response (200 OK):**
```json
{
  "summary": "Property generated $12,450 in revenue over the selected period...",
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-05-06"
  },
  "metrics": [
    {
      "property_id": 1,
      "property_name": "Beachfront Villa",
      "total_revenue": 12450.00,
      "avg_adr": 185.50,
      "avg_occupancy_rate": 75.5,
      "bookings_count": 8
    }
  ],
  "ai_analysis": "The property shows strong performance with consistent bookings...",
  "recommendations": [
    "Consider increasing rates by 5-10% during peak season",
    "Focus on weekend bookings which have higher ADR"
  ],
  "ai_provider": "openai",
  "ai_model": "gpt-3.5-turbo"
}
```

### Top Properties

**Endpoint:** `GET /revenue-analysis/top-properties`

Get ranked list of properties by metric.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `metric`: "revenue", "adr", or "occupancy_rate" (default: "revenue")
- `limit`: Number of properties (1-20, default: 5)
- `start_date`: Filter start date (optional)
- `end_date`: Filter end date (optional)

**Response (200 OK):**
```json
{
  "metric": "revenue",
  "period": {
    "start_date": "2024-01-01",
    "end_date": "2024-05-06"
  },
  "properties": [
    {
      "rank": 1,
      "property_id": 1,
      "property_name": "Beachfront Villa",
      "total_revenue": 45600.00,
      "avg_adr": 195.00,
      "occupancy_rate": 82.5
    },
    {
      "rank": 2,
      "property_id": 2,
      "property_name": "Mountain Lodge",
      "total_revenue": 38200.00,
      "avg_adr": 175.00,
      "occupancy_rate": 78.2
    }
  ],
  "total_count": 5
}
```

### Property Trends

**Endpoint:** `GET /revenue-analysis/property/{property_id}/trends`

Get monthly revenue trends for a property.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `months`: Number of months to analyze (1-60, default: 12)

**Response (200 OK):**
```json
{
  "property_id": 1,
  "property_name": "Beachfront Villa",
  "trend_data": [
    {
      "month": "2024-01",
      "revenue": 3200.00,
      "adr": 160.00,
      "occupancy_rate": 65.0,
      "bookings": 2
    },
    {
      "month": "2024-02",
      "revenue": 4100.00,
      "adr": 175.00,
      "occupancy_rate": 72.5,
      "bookings": 3
    }
  ],
  "avg_monthly_revenue": 3850.00,
  "growth_rate": 28.5,
  "peak_month": "2024-05",
  "slowest_month": "2024-01",
  "ai_analysis": "Strong seasonal pattern detected..."
}
```

---

## Quote Builder

### Generate Quote

**Endpoint:** `POST /revenue-analysis/quotes/generate`

Generate pricing recommendation using historical data and AI reasoning.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "property_id": 1,
  "arrival_date": "2024-06-15",
  "departure_date": "2024-06-22",
  "guest_count": 4,
  "guest_type": "family",
  "apply_seasonal": true,
  "apply_fees": true,
  "ai_provider": "openai"
}
```

**Response (200 OK):**
```json
{
  "quote_id": 42,
  "property_id": 1,
  "property_name": "Beachfront Villa",
  "arrival_date": "2024-06-15",
  "departure_date": "2024-06-22",
  "nights": 7,
  "guest_count": 4,
  "guest_type": "family",
  "base_adr": 150.00,
  "seasonal_multiplier": 1.20,
  "guest_type_factor": 1.10,
  "length_of_stay_factor": 0.95,
  "base_rate": 198.00,
  "cleaning_fee": 100.00,
  "service_fee": 138.60,
  "pet_fee": 0.00,
  "taxes": 190.23,
  "conservative_rate": 168.30,
  "conservative_total": 1489.73,
  "recommended_rate": 198.00,
  "recommended_total": 1626.73,
  "aggressive_rate": 237.60,
  "aggressive_total": 1886.73,
  "ai_reasoning": "Peak summer season with family group justifies premium rates...",
  "status": "draft",
  "created_at": "2024-05-06T12:00:00Z",
  "created_by": 1,
  "ai_provider": "openai",
  "ai_model": "gpt-3.5-turbo"
}
```

### Get Quote

**Endpoint:** `GET /revenue-analysis/quotes/{quote_id}`

Retrieve a specific quote.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** Same as Generate Quote response

### Customize Quote

**Endpoint:** `POST /revenue-analysis/quotes/{quote_id}/customize`

Update quote with staff customization (override rates, add notes).

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request:**
```json
{
  "staff_notes": "Client is loyal, offered 5% discount",
  "override_rate": 185.00,
  "add_fees": {
    "pet_fee": 50.00
  }
}
```

**Response:** Updated quote response with customizations applied

### Quote History

**Endpoint:** `GET /revenue-analysis/quotes`

Get quote history with filtering.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `property_id`: Filter by property (optional)
- `status_filter`: "all", "draft", "sent", "accepted", "rejected" (optional)
- `limit`: Max results (1-200, default: 50)

**Response (200 OK):**
```json
{
  "quotes": [
    {
      "id": 42,
      "property_id": 1,
      "property_name": "Beachfront Villa",
      "guest_count": 4,
      "guest_type": "family",
      "nights": 7,
      "arrival_date": "2024-06-15",
      "departure_date": "2024-06-22",
      "recommended_rate": 198.00,
      "recommended_total": 1626.73,
      "status": "draft",
      "created_at": "2024-05-06T12:00:00Z",
      "created_by": 1
    }
  ],
  "total": 1,
  "limit": 50
}
```

---

## Error Handling

All errors follow a consistent format:

**Error Response Format:**
```json
{
  "detail": "Human-readable error message",
  "code": "ERROR_CODE",
  "request_id": "uuid-for-debugging"
}
```

### Common Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid request parameters |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` | Resource already exists |
| 422 | `UNPROCESSABLE_ENTITY` | Validation failed |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error |

### Example Error Response

**Status 401 Unauthorized:**
```json
{
  "detail": "Not authenticated",
  "code": "UNAUTHORIZED"
}
```

**Status 422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "guest_count"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ],
  "code": "VALIDATION_ERROR"
}
```

---

## Rate Limiting

API endpoints are rate limited to prevent abuse:

- **Default**: 100 requests per minute per user
- **Premium**: Unlimited (when implemented)

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1620000000
```

---

## Interactive API Documentation

Access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide live API testing capabilities.

---

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `skip`: Number of items to skip (default: 0)
- `limit`: Max items to return (default: 50, max: 200)

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 50
}
```

---

## Timestamps

All timestamps are in ISO 8601 format with UTC timezone:
```
2024-05-06T10:00:00Z
```

---

For more information, see the [README](../README.md) or [Development Guide](../DEVELOPMENT.md).
