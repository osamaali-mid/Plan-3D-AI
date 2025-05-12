
import os
import shutil
import uuid
from pydantic import BaseModel
from typing import List
from fastapi import File, UploadFile, HTTPException, APIRouter
from fastapi.responses import FileResponse
from .mock_detection import load_model, detect_objects
from .preprocess import preprocess_image

# Define the directories
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "uploads")
PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "output")

# Create Pydantic models for API
class DetectionResult(BaseModel):
    id: str
    filename: str
    elements: dict
    image_url: str


class FloorplanElement(BaseModel):
    type: str
    confidence: float
    coordinates: List[List[float]]


router = APIRouter(prefix="/api/floorplan", tags=["floorplan"])

# Load the Mask R-CNN model once at startup
model = None

def get_model():
    global model
    if model is None:
        try:
            model = load_model()
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
    return model

def process_floorplan_image(file_path):
    """Process a floorplan image and return detection results"""
    try:
        # Generate unique IDs for processed files
        file_id = str(uuid.uuid4())
        processed_path = os.path.join(PROCESSED_DIR, f"{file_id}_preprocessed.png")
        output_path = os.path.join(OUTPUT_DIR, f"{file_id}_detected.jpg")
        
        # Step 1: Preprocess the image
        preprocess_image(file_path, processed_path)
        
        # Step 2: Load model and perform detection
        model = get_model()
        
        # Step 3: Detect objects
        results = detect_objects(processed_path, output_path, model, return_json=True)
        
        # Return results
        return {
            "id": file_id,
            "filename": os.path.basename(file_path),
            "elements": results,
            "image_url": f"/api/floorplan/images/{file_id}_detected.jpg"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing floorplan: {str(e)}")

@router.post("/detect", response_model=DetectionResult)
async def detect_floorplan(file: UploadFile = File(...)):
    """Upload and process a floorplan image"""
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    temp_file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")
    
    try:
        # Save the uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the floorplan image
        result = process_floorplan_image(temp_file_path)
        
        return result
    
    except Exception as e:
        # Clean up if error occurs
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing the floorplan: {str(e)}")


@router.get("/results/{result_id}")
def get_floorplan_result(result_id: str):
    """Get the results of a specific floorplan detection"""
    output_file = os.path.join(OUTPUT_DIR, f"{result_id}_detected.jpg")
    
    if not os.path.exists(output_file):
        raise HTTPException(status_code=404, detail="Result not found")
    
    return FileResponse(output_file)

