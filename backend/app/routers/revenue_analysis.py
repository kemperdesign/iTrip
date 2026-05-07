from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import logging
from app.database import get_db
from app.models import User, Property, QuoteRecommendation
from app.middleware.auth import get_current_active_user
from app.services.revenue_analysis_service import (
    analyze_revenue,
    get_top_properties,
    get_property_trends,
    generate_quote,
)
from app.schemas import (
    RevenueAnalysisRequest,
    RevenueAnalysisResponse,
    TopPropertiesResponse,
    PropertyTrendResponse,
    QuoteRequest,
    QuoteResponse,
    SavedQuoteResponse,
)
from app.utils.errors import (
    NotFoundError,
    ValidationError,
    InternalServerError,
    log_error,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/revenue-analysis", tags=["revenue_analysis"])


@router.post("/analyze", response_model=RevenueAnalysisResponse)
async def analyze_revenue_endpoint(
    request: RevenueAnalysisRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Analyze revenue for property or all properties with AI insights."""
    try:
        if request.property_id:
            property_exists = db.query(Property).filter(Property.id == request.property_id).first()
            if not property_exists:
                raise NotFoundError("Property", request.property_id)

        result = analyze_revenue(
            db=db,
            property_id=request.property_id,
            start_date=request.start_date,
            end_date=request.end_date,
            ai_provider=getattr(request, "ai_provider", None),
            include_trends=True,
        )
        return result
    except NotFoundError:
        raise
    except ValueError as e:
        log_error("analyze_revenue", e)
        raise ValidationError(str(e))
    except Exception as e:
        log_error("analyze_revenue", e)
        raise InternalServerError(f"Failed to analyze revenue: {str(e)}")


@router.get("/top-properties", response_model=TopPropertiesResponse)
async def get_top_properties_endpoint(
    metric: str = Query("revenue", enum=["revenue", "adr", "occupancy_rate"]),
    limit: int = Query(5, ge=1, le=20),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get top N properties by metric."""
    try:
        if start_date and end_date and start_date > end_date:
            raise ValidationError("start_date must be before end_date")

        result = get_top_properties(
            db=db,
            metric=metric,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        )
        return result
    except ValidationError:
        raise
    except Exception as e:
        log_error("get_top_properties", e)
        raise InternalServerError(f"Failed to get top properties: {str(e)}")


@router.get("/property/{property_id}/trends", response_model=PropertyTrendResponse)
async def get_property_trends_endpoint(
    property_id: int,
    months: int = Query(12, ge=1, le=60),
    ai_provider: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get revenue trends for specific property."""
    try:
        property_exists = db.query(Property).filter(Property.id == property_id).first()
        if not property_exists:
            raise NotFoundError("Property", property_id)

        result = get_property_trends(
            db=db,
            property_id=property_id,
            months=months,
            ai_provider=ai_provider,
        )
        return result
    except NotFoundError:
        raise
    except Exception as e:
        log_error("get_property_trends", e)
        raise InternalServerError(f"Failed to get property trends: {str(e)}")


@router.post("/quotes/generate", response_model=QuoteResponse)
async def generate_quote_endpoint(
    request: QuoteRequest,
    ai_provider: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Generate advanced pricing recommendation with seasonal/guest adjustments."""
    try:
        result = generate_quote(
            db=db,
            property_id=request.property_id,
            check_in_date=request.arrival_date,
            check_out_date=request.departure_date,
            guest_count=request.guest_count,
            guest_type=request.guest_type or "standard",
            apply_seasonal=request.apply_seasonal if hasattr(request, "apply_seasonal") else True,
            apply_fees=request.apply_fees if hasattr(request, "apply_fees") else True,
            ai_provider=ai_provider,
            created_by_user_id=current_user.id,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quote: {str(e)}",
        )


@router.get("/quotes/{quote_id}", response_model=QuoteResponse)
async def get_quote(
    quote_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a saved quote by ID."""
    try:
        quote = db.query(QuoteRecommendation).filter(QuoteRecommendation.id == quote_id).first()
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quote {quote_id} not found",
            )

        prop = db.query(Property).filter(Property.id == quote.property_id).first()
        prop_name = prop.name if prop else f"Property {quote.property_id}"

        return {
            "quote_id": quote.id,
            "property_id": quote.property_id,
            "property_name": prop_name,
            "check_in_date": quote.arrival_date.isoformat(),
            "check_out_date": quote.departure_date.isoformat(),
            "nights": quote.nights,
            "guest_count": quote.guest_count,
            "guest_type": quote.guest_type,
            "base_adr": quote.base_adr,
            "seasonal_multiplier": quote.seasonal_multiplier,
            "guest_type_factor": quote.guest_type_factor,
            "length_of_stay_factor": quote.length_of_stay_factor,
            "base_rate": quote.base_rate,
            "cleaning_fee": quote.cleaning_fee,
            "service_fee": quote.service_fee,
            "pet_fee": quote.pet_fee,
            "taxes": quote.taxes,
            "conservative_rate": quote.conservative_rate,
            "recommended_rate": quote.recommended_rate,
            "aggressive_rate": quote.aggressive_rate,
            "conservative_total": quote.conservative_total,
            "recommended_total": quote.recommended_total,
            "aggressive_total": quote.aggressive_total,
            "status": quote.status,
            "reasoning": quote.reasoning,
            "ai_provider": "openai",
            "ai_model": "gpt-4o-mini",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get quote: {str(e)}",
        )


@router.post("/quotes/{quote_id}/customize", response_model=QuoteResponse)
async def customize_quote(
    quote_id: int,
    staff_notes: Optional[str] = None,
    override_rate: Optional[float] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Customize and update a quote with staff overrides."""
    try:
        quote = db.query(QuoteRecommendation).filter(QuoteRecommendation.id == quote_id).first()
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quote {quote_id} not found",
            )

        # Update with customizations
        if staff_notes:
            quote.staff_notes = staff_notes
        if override_rate is not None:
            quote.staff_override_rate = override_rate
            quote.recommended_rate = override_rate
            quote.recommended_total = override_rate * quote.nights + quote.cleaning_fee + quote.service_fee + quote.taxes

        quote.status = "customized"
        db.commit()
        db.refresh(quote)

        return {
            "quote_id": quote.id,
            "property_id": quote.property_id,
            "property_name": f"Property {quote.property_id}",
            "check_in_date": quote.arrival_date.isoformat(),
            "check_out_date": quote.departure_date.isoformat(),
            "nights": quote.nights,
            "guest_count": quote.guest_count,
            "guest_type": quote.guest_type,
            "base_adr": quote.base_adr,
            "seasonal_multiplier": quote.seasonal_multiplier,
            "guest_type_factor": quote.guest_type_factor,
            "length_of_stay_factor": quote.length_of_stay_factor,
            "base_rate": quote.base_rate,
            "cleaning_fee": quote.cleaning_fee,
            "service_fee": quote.service_fee,
            "pet_fee": quote.pet_fee,
            "taxes": quote.taxes,
            "conservative_rate": quote.conservative_rate,
            "recommended_rate": quote.recommended_rate,
            "aggressive_rate": quote.aggressive_rate,
            "conservative_total": quote.conservative_total,
            "recommended_total": quote.recommended_total,
            "aggressive_total": quote.aggressive_total,
            "status": quote.status,
            "reasoning": quote.reasoning or "Customized quote",
            "ai_provider": "openai",
            "ai_model": "gpt-4o-mini",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to customize quote: {str(e)}",
        )


@router.get("/quotes", response_model=List[SavedQuoteResponse])
async def get_quote_history(
    property_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get quote history with filtering."""
    try:
        query = db.query(QuoteRecommendation)

        if property_id:
            query = query.filter(QuoteRecommendation.property_id == property_id)
        if status_filter:
            query = query.filter(QuoteRecommendation.status == status_filter)

        quotes = query.order_by(QuoteRecommendation.created_at.desc()).limit(limit).all()

        return [
            SavedQuoteResponse(
                id=q.id,
                property_id=q.property_id,
                property_name=f"Property {q.property_id}",
                guest_count=q.guest_count,
                guest_type=q.guest_type,
                nights=q.nights,
                arrival_date=q.arrival_date,
                departure_date=q.departure_date,
                recommended_rate=q.recommended_rate,
                recommended_total=q.recommended_total,
                status=q.status,
                created_at=q.created_at,
            )
            for q in quotes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get quote history: {str(e)}",
        )
