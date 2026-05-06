from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from app.models import RevenueData, Property, QuoteRecommendation
from app.config import settings
from app.services.embeddings import search_similar
import openai
import anthropic


def analyze_revenue(
    db: Session,
    property_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    ai_provider: Optional[str] = None,
    include_trends: bool = True,
) -> Dict[str, Any]:
    """Analyze revenue data for property or all properties with AI insights."""

    # Default date range to last 12 months
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        start_date = end_date - timedelta(days=365)

    # Build query
    query = db.query(RevenueData).filter(
        RevenueData.date >= start_date,
        RevenueData.date <= end_date,
    )

    if property_id:
        query = query.filter(RevenueData.property_id == property_id)

    revenue_records = query.all()

    # Aggregate metrics
    total_revenue = sum(r.revenue for r in revenue_records if r.revenue)
    avg_adr = sum(r.adr for r in revenue_records if r.adr) / len([r for r in revenue_records if r.adr]) if any(r.adr for r in revenue_records) else 0
    avg_occupancy = sum(r.occupancy_rate for r in revenue_records if r.occupancy_rate) / len([r for r in revenue_records if r.occupancy_rate]) if any(r.occupancy_rate for r in revenue_records) else 0

    # Get property details
    metrics = []
    if property_id:
        prop = db.query(Property).filter(Property.id == property_id).first()
        if prop:
            metrics.append({
                "property_id": prop.id,
                "property_name": prop.name,
                "total_revenue": total_revenue,
                "avg_adr": avg_adr,
                "avg_occupancy_rate": avg_occupancy,
                "bookings_count": len(revenue_records),
            })
    else:
        # Group by property
        prop_data = {}
        for record in revenue_records:
            if record.property_id not in prop_data:
                prop = db.query(Property).filter(Property.id == record.property_id).first()
                prop_data[record.property_id] = {
                    "property": prop,
                    "revenue": 0,
                    "adr_sum": 0,
                    "occ_sum": 0,
                    "adr_count": 0,
                    "occ_count": 0,
                    "count": 0,
                }

            prop_data[record.property_id]["count"] += 1
            if record.revenue:
                prop_data[record.property_id]["revenue"] += record.revenue
            if record.adr:
                prop_data[record.property_id]["adr_sum"] += record.adr
                prop_data[record.property_id]["adr_count"] += 1
            if record.occupancy_rate:
                prop_data[record.property_id]["occ_sum"] += record.occupancy_rate
                prop_data[record.property_id]["occ_count"] += 1

        for prop_id, data in prop_data.items():
            if data["property"]:
                metrics.append({
                    "property_id": prop_id,
                    "property_name": data["property"].name,
                    "total_revenue": data["revenue"],
                    "avg_adr": data["adr_sum"] / data["adr_count"] if data["adr_count"] > 0 else 0,
                    "avg_occupancy_rate": data["occ_sum"] / data["occ_count"] if data["occ_count"] > 0 else 0,
                    "bookings_count": data["count"],
                })

    # Calculate trends (monthly)
    trends = {}
    if include_trends:
        current = start_date
        while current < end_date:
            month_start = current.replace(day=1)
            if current.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1)

            month_key = month_start.strftime("%Y-%m")
            month_records = [r for r in revenue_records if month_start <= r.date < month_end]

            if month_records:
                trends[month_key] = {
                    "revenue": sum(r.revenue for r in month_records if r.revenue),
                    "adr": sum(r.adr for r in month_records if r.adr) / len([r for r in month_records if r.adr]) if any(r.adr for r in month_records) else 0,
                    "occupancy_rate": sum(r.occupancy_rate for r in month_records if r.occupancy_rate) / len([r for r in month_records if r.occupancy_rate]) if any(r.occupancy_rate for r in month_records) else 0,
                    "bookings": len(month_records),
                }

            current = month_end

    # Generate AI insights
    data_summary = f"Total Revenue: ${total_revenue:,.2f}, Avg ADR: ${avg_adr:,.2f}, Avg Occupancy: {avg_occupancy:.1%}"
    ai_analysis = _get_ai_response(
        system_prompt="You are a revenue analyst for vacation rental properties. Analyze the provided revenue data and provide actionable insights and recommendations.",
        user_prompt=f"Analyze this revenue data for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}: {data_summary}. Provide 2-3 key insights and recommendations.",
        ai_provider=ai_provider,
    )

    return {
        "summary": data_summary,
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
        "metrics": metrics,
        "trends": trends,
        "ai_analysis": ai_analysis,
        "recommendations": extract_recommendations(ai_analysis),
        "ai_provider": ai_provider or settings.ai_provider,
        "ai_model": get_model_name(ai_provider or settings.ai_provider),
    }


def get_top_properties(
    db: Session,
    metric: str = "revenue",
    limit: int = 5,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Get top N properties by metric."""

    if not end_date:
        end_date = datetime.now()
    if not start_date:
        start_date = end_date - timedelta(days=365)

    # Query aggregated revenue by property
    query = db.query(
        RevenueData.property_id,
        func.sum(RevenueData.revenue).label("total_revenue"),
        func.avg(RevenueData.adr).label("avg_adr"),
        func.avg(RevenueData.occupancy_rate).label("avg_occupancy"),
        func.count(RevenueData.id).label("record_count"),
    ).filter(
        RevenueData.date >= start_date,
        RevenueData.date <= end_date,
    ).group_by(RevenueData.property_id)

    # Order by metric
    if metric == "revenue":
        query = query.order_by(func.sum(RevenueData.revenue).desc())
    elif metric == "adr":
        query = query.order_by(func.avg(RevenueData.adr).desc())
    elif metric == "occupancy_rate":
        query = query.order_by(func.avg(RevenueData.occupancy_rate).desc())

    results = query.limit(limit).all()

    properties = []
    for rank, result in enumerate(results, 1):
        prop = db.query(Property).filter(Property.id == result.property_id).first()
        if prop:
            properties.append({
                "rank": rank,
                "property_id": result.property_id,
                "property_name": prop.name,
                "total_revenue": result.total_revenue,
                "avg_adr": result.avg_adr,
                "avg_occupancy_rate": result.avg_occupancy,
                "record_count": result.record_count,
            })

    return {
        "metric": metric,
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
        "properties": properties,
        "total_count": len(properties),
    }


def get_property_trends(
    db: Session,
    property_id: int,
    months: int = 12,
    ai_provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Get revenue trends for a property (last N months)."""

    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)

    # Query revenue data
    records = db.query(RevenueData).filter(
        RevenueData.property_id == property_id,
        RevenueData.date >= start_date,
        RevenueData.date <= end_date,
    ).order_by(RevenueData.date).all()

    # Group by month
    trend_data = {}
    for record in records:
        month_key = record.date.strftime("%Y-%m")
        if month_key not in trend_data:
            trend_data[month_key] = {
                "month": month_key,
                "revenue": 0,
                "adr": 0,
                "occupancy_rate": 0,
                "bookings": 0,
                "adr_count": 0,
                "occ_count": 0,
            }

        trend_data[month_key]["bookings"] += 1
        if record.revenue:
            trend_data[month_key]["revenue"] += record.revenue
        if record.adr:
            trend_data[month_key]["adr"] += record.adr
            trend_data[month_key]["adr_count"] += 1
        if record.occupancy_rate:
            trend_data[month_key]["occupancy_rate"] += record.occupancy_rate
            trend_data[month_key]["occ_count"] += 1

    # Normalize averages
    for month_key in trend_data:
        if trend_data[month_key]["adr_count"] > 0:
            trend_data[month_key]["adr"] /= trend_data[month_key]["adr_count"]
        if trend_data[month_key]["occ_count"] > 0:
            trend_data[month_key]["occupancy_rate"] /= trend_data[month_key]["occ_count"]
        del trend_data[month_key]["adr_count"]
        del trend_data[month_key]["occ_count"]

    sorted_trends = sorted(trend_data.values(), key=lambda x: x["month"])

    # Calculate aggregate metrics
    total_revenue = sum(t["revenue"] for t in sorted_trends)
    avg_monthly_revenue = total_revenue / len(sorted_trends) if sorted_trends else 0

    # Calculate growth rate
    if len(sorted_trends) >= 2:
        first_month_revenue = sorted_trends[0]["revenue"]
        last_month_revenue = sorted_trends[-1]["revenue"]
        growth_rate = ((last_month_revenue - first_month_revenue) / first_month_revenue * 100) if first_month_revenue > 0 else 0
    else:
        growth_rate = 0

    # Find peak and slowest months
    peak_month = max(sorted_trends, key=lambda x: x["revenue"])["month"] if sorted_trends else "N/A"
    slowest_month = min(sorted_trends, key=lambda x: x["revenue"])["month"] if sorted_trends else "N/A"

    # Get property name
    prop = db.query(Property).filter(Property.id == property_id).first()
    prop_name = prop.name if prop else f"Property {property_id}"

    # Generate AI analysis
    ai_analysis = None
    if ai_provider:
        data_summary = f"Peak Month: {peak_month} (${max(t['revenue'] for t in sorted_trends if t['revenue']):,.2f}), Growth Rate: {growth_rate:.1f}%"
        ai_analysis = _get_ai_response(
            system_prompt="You are a revenue analyst for vacation rental properties. Provide insights on property performance trends.",
            user_prompt=f"Analyze these trends for {prop_name}: {data_summary}. Provide 2-3 key insights.",
            ai_provider=ai_provider,
        )

    return {
        "property_id": property_id,
        "property_name": prop_name,
        "trend_data": sorted_trends,
        "avg_monthly_revenue": avg_monthly_revenue,
        "growth_rate": growth_rate,
        "peak_month": peak_month,
        "slowest_month": slowest_month,
        "ai_analysis": ai_analysis,
        "ai_provider": ai_provider or settings.ai_provider,
    }


def generate_quote(
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
    """Generate pricing recommendation with seasonal/guest adjustments.

    This function now delegates to pricing_service.generate_advanced_quote()
    which handles all calculations and persists to database.
    """
    from app.services.pricing_service import generate_advanced_quote as pricing_generate_quote

    return pricing_generate_quote(
        db=db,
        property_id=property_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        guest_count=guest_count,
        guest_type=guest_type,
        apply_seasonal=apply_seasonal,
        apply_fees=apply_fees,
        ai_provider=ai_provider,
        created_by_user_id=created_by_user_id,
    )


def _get_ai_response(
    system_prompt: str,
    user_prompt: str,
    ai_provider: Optional[str] = None,
) -> str:
    """Route to appropriate AI provider (OpenAI, Anthropic, Gemini)."""
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
    """Generate analysis using OpenAI GPT."""
    try:
        client = openai.OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.ai_model or "gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


def _anthropic_response(system_prompt: str, user_prompt: str) -> str:
    """Generate analysis using Anthropic Claude."""
    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=500,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


def _gemini_response(system_prompt: str, user_prompt: str) -> str:
    """Generate analysis using Google Gemini."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{system_prompt}\n\n{user_prompt}")
        return response.text
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


def extract_recommendations(text: str) -> List[str]:
    """Extract recommendations from AI analysis text."""
    recommendations = []
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line and (line.startswith("-") or line.startswith("•") or line.startswith("•")):
            recommendations.append(line.lstrip("-•").strip())
    return recommendations[:5]  # Return top 5


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
