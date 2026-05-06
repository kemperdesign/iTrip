import pytest
from datetime import datetime, timedelta
from app.services.pricing_service import (
    calculate_seasonal_multiplier,
    calculate_guest_type_factor,
    calculate_length_of_stay_factor,
)


class TestSeasonalMultiplier:
    """Test seasonal pricing multiplier calculations."""

    def test_summer_season_premium(self):
        """Test summer (June-Aug) gets 20% premium."""
        date = datetime(2026, 7, 15).date()  # July
        multiplier = calculate_seasonal_multiplier(date)
        assert multiplier == 1.2, f"Expected 1.2 for summer, got {multiplier}"

    def test_winter_holidays_premium(self):
        """Test winter holidays (Dec 20-Jan 2) get 30% premium."""
        dates = [
            datetime(2025, 12, 25).date(),  # Christmas
            datetime(2026, 1, 1).date(),    # New Year
        ]
        for date in dates:
            multiplier = calculate_seasonal_multiplier(date)
            assert multiplier == 1.3, f"Expected 1.3 for winter holidays, got {multiplier}"

    def test_spring_break_premium(self):
        """Test spring break (Mar-Apr) gets 15% premium."""
        date = datetime(2026, 3, 15).date()  # March
        multiplier = calculate_seasonal_multiplier(date)
        assert multiplier == 1.15, f"Expected 1.15 for spring break, got {multiplier}"

    def test_off_season_discount(self):
        """Test off-season gets 30% discount."""
        date = datetime(2026, 11, 15).date()  # November
        multiplier = calculate_seasonal_multiplier(date)
        assert multiplier == 0.7, f"Expected 0.7 for off-season, got {multiplier}"

    def test_regular_season_baseline(self):
        """Test regular season (no holiday) uses baseline."""
        date = datetime(2026, 5, 15).date()  # May
        multiplier = calculate_seasonal_multiplier(date)
        assert multiplier == 1.0, f"Expected 1.0 for regular season, got {multiplier}"


class TestGuestTypeFactor:
    """Test guest type pricing factors."""

    def test_family_premium(self):
        """Test family (4+ guests) gets 10% premium."""
        factor = calculate_guest_type_factor(4, "family")
        assert factor == 1.1, f"Expected 1.1 for family, got {factor}"

    def test_couple_baseline(self):
        """Test couple (2 guests) uses baseline."""
        factor = calculate_guest_type_factor(2, "couple")
        assert factor == 1.0, f"Expected 1.0 for couple, got {factor}"

    def test_large_group_discount(self):
        """Test large group (8+ guests) gets 10% discount."""
        factor = calculate_guest_type_factor(8, "group")
        assert factor == 0.9, f"Expected 0.9 for large group, got {factor}"

    def test_solo_traveler_premium(self):
        """Test solo traveler gets 5% premium."""
        factor = calculate_guest_type_factor(1, "solo")
        assert factor == 1.05, f"Expected 1.05 for solo, got {factor}"


class TestLengthOfStayFactor:
    """Test length of stay pricing factors."""

    def test_weekly_discount(self):
        """Test 7-night stay gets 10% discount."""
        factor = calculate_length_of_stay_factor(7)
        assert factor == 0.9, f"Expected 0.9 for weekly, got {factor}"

    def test_monthly_discount(self):
        """Test 28+ night stay gets 20% discount."""
        factor = calculate_length_of_stay_factor(30)
        assert factor == 0.8, f"Expected 0.8 for monthly, got {factor}"

    def test_weekend_premium(self):
        """Test 2-3 night stay (weekend) gets 5% premium."""
        factor = calculate_length_of_stay_factor(2)
        assert factor == 1.05, f"Expected 1.05 for weekend, got {factor}"

    def test_standard_stay_baseline(self):
        """Test standard 4-6 night stay uses baseline."""
        factor = calculate_length_of_stay_factor(5)
        assert factor == 1.0, f"Expected 1.0 for standard, got {factor}"
