#!/usr/bin/env python3
"""
Simple FastAPI server for floorplan detection without heavy dependencies
"""
import os
import shutil
import uuid
from typing import List, Optional
import sys
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Floorplan Recognition API")

# Add floorplan module to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Create necessary directories
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data", "uploads")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "output")

# Ensure directories exist
for directory in [UPLOAD_DIR, PROCESSED_DIR, OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)

# Create Pydantic models for API
class DetectionResult(BaseModel):
    id: str
    filename: str
    elements: dict
    image_url: str

# Import floor plan processing functions
try:
    from app.floorplan.preprocess import preprocess_image
    from app.floorplan.mock_detection import load_model, detect_objects
    PROCESSING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import processing modules: {e}")
    PROCESSING_AVAILABLE = False

# Load the model once at startup
model = None

def get_model():
    global model
    if model is None and PROCESSING_AVAILABLE:
        try:
            model = load_model()
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
    return model

def process_floorplan_image(file_path):
    """Process a floorplan image and return detection results"""
    if not PROCESSING_AVAILABLE:
        # Return mock results if processing is not available
        file_id = str(uuid.uuid4())
        return {
            "id": file_id,
            "filename": os.path.basename(file_path),
            "elements": {
                "walls": [{"type": "Wall", "confidence": 0.95, "bbox": [10, 10, 100, 100], "contour": [[10, 10], [100, 10], [100, 100], [10, 100]]}],
                "windows": [{"type": "Window", "confidence": 0.88, "bbox": [50, 50, 80, 80], "contour": [[50, 50], [80, 50], [80, 80], [50, 80]]}],
                "doors": [{"type": "Door", "confidence": 0.92, "bbox": [20, 20, 60, 60], "contour": [[20, 20], [60, 20], [60, 60], [20, 60]]}]
            },
            "image_url": f"/api/floorplan/images/mock_detected.jpg"
        }
    
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files directory for serving images
app.mount("/api/floorplan/images", StaticFiles(directory=OUTPUT_DIR), name="floorplan_images")

@app.get("/health")
def health():
    return {"status": "UP", "processing_available": PROCESSING_AVAILABLE}

@app.post("/api/floorplan/detect", response_model=DetectionResult)
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

@app.get("/api/floorplan/results/{result_id}")
def get_floorplan_result(result_id: str):
    """Get the results of a specific floorplan detection"""
    output_file = os.path.join(OUTPUT_DIR, f"{result_id}_detected.jpg")
    
    if not os.path.exists(output_file):
        raise HTTPException(status_code=404, detail="Result not found")
    
    return FileResponse(output_file)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)