from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models import RevenueData, Property, QuoteRecommendation, User
from app.config import settings
import openai
import anthropic


# Holiday calendar configuration
HOLIDAYS = {
    "christmas": (12, 20, 1, 2),  # Dec 20 - Jan 2
    "spring_break": (3, 10, 4, 15),  # Mar 10 - Apr 15
    "independence_day": (7, 1, 7, 4),  # Jul 1-4
    "thanksgiving": (11, 20, 11, 28),  # Nov 20-28
}

# Seasonal multipliers
SEASONAL_MULTIPLIERS = {
    "summer": (6, 8, 1.20),  # June-Aug: +20%
    "winter_peak": (12, 1, 1.25),  # Dec-Jan: +25%
    "spring_break": (3, 4, 1.15),  # Mar-Apr: +15%
    "off_season": (1, 5, 0.80),  # Jan-May: -20% (simplified)
    "default": 1.0,
}


def calculate_seasonal_multiplier(check_in_date: datetime) -> float:
    """
    Calculate seasonal pricing multiplier based on date.
    Returns multiplier between 0.7 and 1.3.
    """
    month = check_in_date.month
    day = check_in_date.day

    # Check specific holidays first
    if _is_holiday_period(month, day, HOLIDAYS["christmas"]):
        return 1.30  # Peak: Winter holidays
    if _is_holiday_period(month, day, HOLIDAYS["spring_break"]):
        return 1.15  # High: Spring break
    if _is_holiday_period(month, day, HOLIDAYS["independence_day"]):
        return 1.20  # Peak: Independence Day
    if _is_holiday_period(month, day, HOLIDAYS["thanksgiving"]):
        return 1.20  # Peak: Thanksgiving

    # Check seasonal periods
    if month in (6, 7, 8):  # June-August: Summer peak
        return 1.20
    if month in (12, 1):  # Dec-Jan: Winter peak
        return 1.25
    if month in (3, 4):  # Mar-Apr: Spring break season
        return 1.15
    if month in (9, 10):  # Sep-Oct: Fall, moderate
        return 1.05
    if month in (2, 5):  # Feb, May: Shoulder seasons
        return 0.95
    if month in (1, 11):  # Jan, Nov: Off-season
        return 0.85

    return 1.0  # Default


def calculate_guest_type_factor(guest_count: int, guest_type: str = "standard") -> float:
    """
    Calculate pricing adjustment based on guest type and count.
    Returns multiplier between 0.8 and 1.15.
    """
    if guest_type == "family":
        # Family (4+ guests): +10% premium for larger occupancy
        if guest_count >= 4:
            return 1.10
    elif guest_type == "couple":
        # Couple (2 guests): baseline
        return 1.0
    elif guest_type == "group":
        # Large group (8+ guests): -10% group discount
        if guest_count >= 8:
            return 0.90
        elif guest_count >= 6:
            return 0.95

    # Fallback logic by count
    if guest_count == 1:  # Solo traveler
        return 1.05  # +5% premium (less occupancy)
    elif guest_count == 2:  # Couple
        return 1.0  # Baseline
    elif guest_count in (3, 4):  # Small family
        return 1.05  # +5% for larger family
    elif guest_count in (5, 6):  # Medium group
        return 1.0  # Neutral
    else:  # Large group (7+)
        return 0.90  # -10% group discount

    return 1.0


def calculate_length_of_stay_factor(nights: int) -> float:
    """
    Calculate pricing adjustment based on length of stay.
    Returns multiplier between 0.8 and 1.05.
    """
    if nights >= 28:  # Monthly stay (28+ nights)
        return 0.80  # -20% discount
    elif nights >= 14:  # Two-week stay
        return 0.90  # -10% discount
    elif nights >= 7:  # Weekly stay
        return 0.95  # -5% discount
    elif nights in (2, 3):  # Weekend
        return 1.05  # +5% premium
    else:  # Standard weekday stay (4-6 nights)
        return 1.0  # Baseline


def calculate_fees(guest_count: int, nights: int, pet_friendly: bool = False) -> Dict[str, float]:
    """
    Calculate standard fees for a quote.
    Returns dict with cleaning_fee, service_fee, pet_fee, taxes.
    """
    fees = {
        "cleaning_fee": 100.0,  # Standard cleaning fee
        "service_fee": 0.0,  # Will be calculated as % of nightly rate
        "pet_fee": 50.0 if pet_friendly else 0.0,
        "taxes": 0.0,  # Will be calculated as % of total
    }
    return fees


def generate_advanced_quote(
    db: Session,
    property_id: int,
    check_in_date: datetime,
    check_out_date: datetime,
    guest_count: int,
    guest_type: str = "standard",
    apply_seasonal: bool = True,
    apply_fees: bool = True,
    ai_provider: Optional[str] = None,
    created_by_user_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a comprehensive quote with all adjustments and persist to database.
    """
    # Calculate basic metrics
    nights = (check_out_date - check_in_date).days

    # Get base ADR from historical data (±14 days)
    start_search = check_in_date - timedelta(days=14)
    end_search = check_out_date + timedelta(days=14)

    historical_records = db.query(RevenueData).filter(
        RevenueData.property_id == property_id,
        RevenueData.date >= start_search,
        RevenueData.date <= end_search,
    ).all()

    # Calculate base ADR
    if historical_records:
        adrs = sorted([r.adr for r in historical_records if r.adr])
        if adrs:
            base_adr = adrs[int(len(adrs) * 0.50)]  # Use median
        else:
            base_adr = 150.0  # Default
    else:
        base_adr = 150.0  # Default if no data

    # Calculate multipliers
    seasonal_mult = calculate_seasonal_multiplier(check_in_date) if apply_seasonal else 1.0
    guest_mult = calculate_guest_type_factor(guest_count, guest_type)
    stay_mult = calculate_length_of_stay_factor(nights)

    # Calculate base rate with multipliers
    adjusted_rate = base_adr * seasonal_mult * guest_mult * stay_mult

    # Calculate percentiles for three tiers
    adjusted_base = adjusted_rate
    conservative_rate = adjusted_base * 0.85  # -15% from adjusted base
    recommended_rate = adjusted_base  # Use adjusted base as recommended
    aggressive_rate = adjusted_base * 1.20  # +20% from adjusted base

    # Add fees if enabled
    fees = calculate_fees(guest_count, nights) if apply_fees else {
        "cleaning_fee": 0.0,
        "service_fee": 0.0,
        "pet_fee": 0.0,
        "taxes": 0.0,
    }

    # Calculate service fee as % of nightly rate
    fees["service_fee"] = recommended_rate * 0.10  # 10% service fee

    # Calculate taxes as % of subtotal
    subtotal = (recommended_rate * nights) + fees["cleaning_fee"] + fees["pet_fee"]
    fees["taxes"] = subtotal * 0.10  # 10% tax

    # Calculate totals
    conservative_total = (conservative_rate * nights) + fees["cleaning_fee"] + fees["service_fee"] + fees["pet_fee"] + (subtotal * 0.10)
    recommended_total = (recommended_rate * nights) + fees["cleaning_fee"] + fees["service_fee"] + fees["pet_fee"] + (subtotal * 0.10)
    aggressive_total = (aggressive_rate * nights) + fees["cleaning_fee"] + fees["service_fee"] + fees["pet_fee"] + (subtotal * 0.10)

    # Get property name
    prop = db.query(Property).filter(Property.id == property_id).first()
    prop_name = prop.name if prop else f"Property {property_id}"

    # Generate AI reasoning
    reasoning = _generate_pricing_reasoning(
        prop_name,
        check_in_date,
        check_out_date,
        nights,
        guest_count,
        guest_type,
        base_adr,
        seasonal_mult,
        guest_mult,
        stay_mult,
        recommended_rate,
        ai_provider,
    )

    # Persist to database
    quote = QuoteRecommendation(
        property_id=property_id,
        arrival_date=check_in_date,
        departure_date=check_out_date,
        nights=nights,
        guest_count=guest_count,
        guest_type=guest_type,
        base_adr=base_adr,
        seasonal_multiplier=seasonal_mult,
        guest_type_factor=guest_mult,
        length_of_stay_factor=stay_mult,
        base_rate=adjusted_base,
        cleaning_fee=fees["cleaning_fee"],
        service_fee=fees["service_fee"],
        pet_fee=fees["pet_fee"],
        taxes=fees["taxes"],
        conservative_rate=conservative_rate,
        recommended_rate=recommended_rate,
        aggressive_rate=aggressive_rate,
        conservative_total=conservative_total,
        recommended_total=recommended_total,
        aggressive_total=aggressive_total,
        reasoning=reasoning,
        status="draft",
        created_by=created_by_user_id,
    )

    db.add(quote)
    db.commit()
    db.refresh(quote)

    return {
        "quote_id": quote.id,
        "property_id": property_id,
        "property_name": prop_name,
        "check_in_date": check_in_date.isoformat(),
        "check_out_date": check_out_date.isoformat(),
        "nights": nights,
        "guest_count": guest_count,
        "guest_type": guest_type,
        "base_adr": base_adr,
        "seasonal_multiplier": seasonal_mult,
        "guest_type_factor": guest_mult,
        "length_of_stay_factor": stay_mult,
        "base_rate": adjusted_base,
        "cleaning_fee": fees["cleaning_fee"],
        "service_fee": fees["service_fee"],
        "pet_fee": fees["pet_fee"],
        "taxes": fees["taxes"],
        "conservative_rate": conservative_rate,
        "recommended_rate": recommended_rate,
        "aggressive_rate": aggressive_rate,
        "conservative_total": conservative_total,
        "recommended_total": recommended_total,
        "aggressive_total": aggressive_total,
        "reasoning": reasoning,
        "status": "draft",
        "ai_provider": ai_provider or settings.ai_provider,
        "ai_model": get_model_name(ai_provider or settings.ai_provider),
    }


def _is_holiday_period(month: int, day: int, date_range: tuple) -> bool:
    """Check if a date falls within a holiday period."""
    start_month, start_day, end_month, end_day = date_range

    if start_month == end_month:
        return month == start_month and start_day <= day <= end_day
    elif start_month < end_month:
        return (month == start_month and day >= start_day) or (month == end_month and day <= end_day)
    else:  # Wraps year
        return (month == start_month and day >= start_day) or (month == end_month and day <= end_day)


def _generate_pricing_reasoning(
    prop_name: str,
    check_in_date: datetime,
    check_out_date: datetime,
    nights: int,
    guest_count: int,
    guest_type: str,
    base_adr: float,
    seasonal_mult: float,
    guest_mult: float,
    stay_mult: float,
    recommended_rate: float,
    ai_provider: Optional[str] = None,
) -> str:
    """Generate AI-powered reasoning for the pricing recommendation."""

    prompt = f"""For {prop_name} from {check_in_date.strftime('%Y-%m-%d')} to {check_out_date.strftime('%Y-%m-%d')} ({nights} nights, {guest_count} {guest_type} guests):

Base ADR: ${base_adr:.2f}
Seasonal Adjustment: {seasonal_mult:.1%}
Guest Type Adjustment: {guest_mult:.1%}
Length of Stay Adjustment: {stay_mult:.1%}
Recommended Rate: ${recommended_rate:.2f}/night

Provide a brief 2-3 sentence explanation of this pricing recommendation, considering the seasonal multiplier, guest composition, and length of stay."""

    return _get_ai_response(
        system_prompt="You are a vacation rental pricing expert. Provide concise, data-driven pricing justifications.",
        user_prompt=prompt,
        ai_provider=ai_provider,
    )


def _get_ai_response(
    system_prompt: str,
    user_prompt: str,
    ai_provider: Optional[str] = None,
) -> str:
    """Route to appropriate AI provider."""
    provider = ai_provider or settings.ai_provider

    if provider == "openai":
        return _openai_response(system_prompt, user_prompt)
    elif provider == "anthropic":
        return _anthropic_response(system_prompt, user_prompt)
    elif provider == "gemini":
        return _gemini_response(system_prompt, user_prompt)
    else:
        return _openai_response(system_prompt, user_prompt)


def _openai_response(system_prompt: str, user_prompt: str) -> str:
    """Generate response using OpenAI."""
    try:
        client = openai.OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.ai_model or "gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Pricing based on seasonal, guest, and occupancy factors. Error generating detailed reasoning: {str(e)}"


def _anthropic_response(system_prompt: str, user_prompt: str) -> str:
    """Generate response using Anthropic Claude."""
    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=300,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"Pricing based on seasonal, guest, and occupancy factors. Error generating detailed reasoning: {str(e)}"


def _gemini_response(system_prompt: str, user_prompt: str) -> str:
    """Generate response using Google Gemini."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        return response.text
    except Exception as e:
        return f"Pricing based on seasonal, guest, and occupancy factors. Error generating detailed reasoning: {str(e)}"


def get_model_name(ai_provider: str) -> str:
    """Get the model name for the given provider."""
    if ai_provider == "openai":
        return settings.ai_model or "gpt-4o-mini"
    elif ai_provider == "anthropic":
        return "claude-opus-4-7"
    elif ai_provider == "gemini":
        return "gemini-1.5-flash"
    else:
        return "unknown"
