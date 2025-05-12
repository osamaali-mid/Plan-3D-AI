import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create a test client fixture"""
    return TestClient(app)

@pytest.fixture
def test_image():
    """Create a test image fixture"""
    # You can create a simple test image here or use a sample image
    return "tests/test_data/sample_floorplan.jpg" 