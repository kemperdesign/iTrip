import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import RevenueData, Property
from app.services.revenue_analysis_service import (
    get_top_properties,
    calculate_date_range_metrics,
)


class TestGetTopProperties:
    """Test top properties ranking by metric."""

    def test_top_properties_by_revenue(self, db_session: Session, sample_dates):
        """Test ranking properties by total revenue."""
        # Setup: Create properties and revenue data
        prop1 = Property(name="Sea Casa", property_type="rental")
        prop2 = Property(name="Mountain Lodge", property_type="rental")
        db_session.add_all([prop1, prop2])
        db_session.commit()

        rev1 = RevenueData(
            property_id=prop1.id,
            revenue=10000,
            adr=200,
            occupancy_rate=0.8,
            year_month="2026-04",
        )
        rev2 = RevenueData(
            property_id=prop2.id,
            revenue=5000,
            adr=150,
            occupancy_rate=0.7,
            year_month="2026-04",
        )
        db_session.add_all([rev1, rev2])
        db_session.commit()

        # Test: Get top 1 by revenue
        results = get_top_properties(
            db_session,
            metric="revenue",
            limit=1,
            start_date=sample_dates["start_date"],
            end_date=sample_dates["end_date"],
        )

        assert len(results) == 1
        assert results[0]["revenue"] == 10000
        assert results[0]["property_name"] == "Sea Casa"

    def test_top_properties_by_adr(self, db_session: Session, sample_dates):
        """Test ranking properties by average daily rate."""
        prop1 = Property(name="Luxury Suite", property_type="rental")
        prop2 = Property(name="Budget Inn", property_type="rental")
        db_session.add_all([prop1, prop2])
        db_session.commit()

        rev1 = RevenueData(
            property_id=prop1.id,
            revenue=8000,
            adr=400,
            occupancy_rate=0.6,
            year_month="2026-04",
        )
        rev2 = RevenueData(
            property_id=prop2.id,
            revenue=6000,
            adr=100,
            occupancy_rate=0.9,
            year_month="2026-04",
        )
        db_session.add_all([rev1, rev2])
        db_session.commit()

        results = get_top_properties(
            db_session,
            metric="adr",
            limit=1,
            start_date=sample_dates["start_date"],
            end_date=sample_dates["end_date"],
        )

        assert len(results) == 1
        assert results[0]["adr"] == 400

    def test_top_properties_limit(self, db_session: Session, sample_dates):
        """Test limit parameter works correctly."""
        # Create 5 properties
        for i in range(5):
            prop = Property(name=f"Property {i}", property_type="rental")
            db_session.add(prop)
        db_session.commit()

        # Add revenue data
        for prop in db_session.query(Property).all():
            rev = RevenueData(
                property_id=prop.id,
                revenue=10000 - (prop.id * 1000),
                adr=200,
                occupancy_rate=0.8,
                year_month="2026-04",
            )
            db_session.add(rev)
        db_session.commit()

        results = get_top_properties(
            db_session,
            metric="revenue",
            limit=3,
            start_date=sample_dates["start_date"],
            end_date=sample_dates["end_date"],
        )

        assert len(results) == 3


class TestCalculateDateRangeMetrics:
    """Test metrics calculation for date ranges."""

    def test_revenue_sum_in_range(self, db_session: Session, sample_dates):
        """Test total revenue calculation."""
        prop = Property(name="Test Property", property_type="rental")
        db_session.add(prop)
        db_session.commit()

        # Add multiple months of data
        for month in ["2026-01", "2026-02", "2026-03"]:
            rev = RevenueData(
                property_id=prop.id,
                revenue=5000,
                adr=200,
                occupancy_rate=0.8,
                year_month=month,
            )
            db_session.add(rev)
        db_session.commit()

        metrics = calculate_date_range_metrics(
            db_session,
            property_id=prop.id,
            start_date=datetime(2026, 1, 1).date(),
            end_date=datetime(2026, 3, 31).date(),
        )

        assert metrics["total_revenue"] == 15000

    def test_average_adr_calculation(self, db_session: Session):
        """Test average ADR calculation."""
        prop = Property(name="Test Property", property_type="rental")
        db_session.add(prop)
        db_session.commit()

        for adr_val in [150, 200, 250]:
            rev = RevenueData(
                property_id=prop.id,
                revenue=5000,
                adr=adr_val,
                occupancy_rate=0.8,
                year_month=f"2026-0{[150, 200, 250].index(adr_val) + 1}",
            )
            db_session.add(rev)
        db_session.commit()

        metrics = calculate_date_range_metrics(
            db_session,
            property_id=prop.id,
            start_date=datetime(2026, 1, 1).date(),
            end_date=datetime(2026, 3, 31).date(),
        )

        assert metrics["avg_adr"] == 200
