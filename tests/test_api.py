import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}

def test_invalid_endpoint():
    """Test invalid endpoint handling"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404

def test_predict_api(tmp_path):
    """Test the predict endpoint with a sample image"""
    # Create a dummy image file
    test_image_path = "tests/test.png"
    with open(test_image_path, "rb") as f:
        response = client.post(
            "/api/floorplan/detect",
            files={"file": ("test.png", f, "image/png")}
        )
    assert response.status_code == 200
    # Optionally, check the response content if you know the expected output
    # assert "prediction" in response.json()

# Add more specific API tests based on your endpoints
# Example:
# def test_floorplan_upload():
#     """Test floorplan upload endpoint"""
#     test_file = "path/to/test/image.jpg"
#     with open(test_file, "rb") as f:
#         response = client.post(
#             "/upload",
#             files={"file": ("test.jpg", f, "image/jpeg")}
#         )
#     assert response.status_code == 200 