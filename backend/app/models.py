from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    max_guests = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    document_type = Column(String)  # property_notes, response_templates, revenue_data, etc.
    content = Column(Text)
    file_hash = Column(String, unique=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PropertyFact(Base):
    __tablename__ = "property_facts"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    fact_type = Column(String)  # wifi, parking, door_code, water_shutoff, etc.
    fact_label = Column(String)
    fact_value = Column(Text)
    source_document = Column(Integer, ForeignKey("documents.id"))
    confidence_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    guest_name = Column(String)
    guest_email = Column(String)
    guest_phone = Column(String)
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    nights = Column(Integer)
    guest_count = Column(Integer)
    booking_source = Column(String)  # VRBO, Airbnb, direct, etc.
    reservation_total = Column(Float)
    status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RevenueData(Base):
    __tablename__ = "revenue_data"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    date = Column(DateTime, index=True)
    revenue = Column(Float)
    adr = Column(Float)  # Average Daily Rate
    occupancy_rate = Column(Float)
    source_document = Column(Integer, ForeignKey("documents.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    guest_name = Column(String)
    guest_message = Column(Text)
    message_category = Column(String)  # wifi, parking, pricing, etc.
    risk_level = Column(String, default="low")  # low, medium, high, escalate
    created_at = Column(DateTime, default=datetime.utcnow)


class AIResponse(Base):
    __tablename__ = "ai_responses"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    response_type = Column(String)  # guest_reply, property_info, revenue_analysis, quote, etc.
    generated_content = Column(Text)
    ai_provider = Column(String)  # gemini, openai, anthropic
    ai_model = Column(String)
    approved_by_user = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuoteRecommendation(Base):
    __tablename__ = "quote_recommendations"

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    arrival_date = Column(DateTime)
    departure_date = Column(DateTime)
    nights = Column(Integer)
    guest_count = Column(Integer)
    conservative_rate = Column(Float)
    recommended_rate = Column(Float)
    aggressive_rate = Column(Float)
    recommended_total = Column(Float)
    reasoning = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
