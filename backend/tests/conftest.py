import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def db_engine():
    """Create in-memory SQLite database for tests."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a fresh database session for each test."""
    TestingSessionLocal = sessionmaker(bind=db_engine)
    session = TestingSessionLocal()

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI test client with overridden database."""
    return TestClient(app)


@pytest.fixture
def sample_dates():
    """Sample dates for quote/revenue testing."""
    today = datetime.now().date()
    return {
        "check_in": today + timedelta(days=7),
        "check_out": today + timedelta(days=14),
        "start_date": today - timedelta(days=90),
        "end_date": today,
    }


@pytest.fixture
def sample_property_data():
    """Sample property data for testing."""
    return {
        "property_id": 1,
        "property_name": "Sea Casa",
        "address": "123 Ocean Drive",
    }
