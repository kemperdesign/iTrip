from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any


# Auth Schemas
class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Document Schemas
class DocumentUpload(BaseModel):
    filename: str
    document_type: str


class DocumentResponse(BaseModel):
    id: int
    filename: str
    document_type: str
    uploaded_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    document_type: str
    status: str
    chunk_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Property Schemas
class PropertyCreate(BaseModel):
    name: str
    address: str
    city: str
    state: str
    bedrooms: int
    bathrooms: int
    max_guests: int


class PropertyResponse(BaseModel):
    id: int
    name: str
    address: str
    city: str
    state: str
    bedrooms: int
    bathrooms: int
    max_guests: int
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Message/Guest Reply Schemas
class GuestMessageCreate(BaseModel):
    property_id: int
    guest_name: str
    guest_message: str


class GuestReplyDraft(BaseModel):
    draft_reply: str
    ai_provider: str
    ai_model: str
    risk_flags: Optional[list] = None


class RiskFlag(BaseModel):
    keyword: str
    risk_level: str
    message_excerpt: str


class GenerateGuestReplyRequest(BaseModel):
    message_id: int
    ai_provider: Optional[str] = None
    include_templates: bool = True
    template_doc_id: Optional[int] = None


class GenerateGuestReplyResponse(BaseModel):
    ai_response_id: int
    reply_text: str
    risk_flags: list[RiskFlag]
    source_templates: list
    ai_provider: str
    ai_model: str
    requires_review: bool


class GuestMessageWithReply(BaseModel):
    message_id: int
    guest_name: str
    guest_message: str
    message_category: Optional[str]
    risk_level: str
    replies: list[GenerateGuestReplyResponse]

    class Config:
        from_attributes = True


# Revenue Schemas
class RevenueAnalysisRequest(BaseModel):
    property_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PropertyRevenueMetrics(BaseModel):
    property_id: int
    property_name: str
    total_revenue: float
    avg_adr: float
    avg_occupancy_rate: float
    bookings_count: int


class RevenueAnalysisResponse(BaseModel):
    summary: str
    period: Dict[str, str]
    metrics: List[PropertyRevenueMetrics]
    trends: Dict[str, Any]
    ai_analysis: str
    recommendations: List[str]
    ai_provider: str
    ai_model: str


class PropertyTrendPoint(BaseModel):
    month: str
    revenue: float
    adr: float
    occupancy_rate: float
    bookings: int


class PropertyTrendResponse(BaseModel):
    property_id: int
    property_name: str
    trend_data: List[PropertyTrendPoint]
    avg_monthly_revenue: float
    growth_rate: float
    peak_month: str
    slowest_month: str
    ai_analysis: Optional[str] = None
    ai_provider: Optional[str] = None


class TopPropertiesResponse(BaseModel):
    metric: str
    period: Dict[str, str]
    properties: List[Dict[str, Any]]
    total_count: int


# Quote Schemas
class QuoteRequest(BaseModel):
    property_id: int
    arrival_date: datetime
    departure_date: datetime
    guest_count: int
    guest_type: Optional[str] = "standard"  # family, couple, group
    apply_seasonal: Optional[bool] = True
    apply_fees: Optional[bool] = True


class QuoteResponse(BaseModel):
    quote_id: int
    property_id: int
    property_name: str
    check_in_date: str
    check_out_date: str
    nights: int
    guest_count: int
    guest_type: str

    # Calculation details
    base_adr: float
    seasonal_multiplier: float
    guest_type_factor: float
    length_of_stay_factor: float
    base_rate: float

    # Fees breakdown
    cleaning_fee: float
    service_fee: float
    pet_fee: float
    taxes: float

    # Rates and totals
    conservative_rate: float
    recommended_rate: float
    aggressive_rate: float
    conservative_total: float
    recommended_total: float
    aggressive_total: float

    # Status and reasoning
    status: str
    reasoning: str
    ai_provider: str
    ai_model: str


class SavedQuoteResponse(BaseModel):
    id: int
    property_id: int
    property_name: str
    guest_count: int
    guest_type: str
    nights: int
    arrival_date: datetime
    departure_date: datetime
    recommended_rate: float
    recommended_total: float
    status: str
    created_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True
