import pytest
from src.myapp import app

@pytest.fixture
def client():
    """A test client for the app."""
    return app.test_client()
