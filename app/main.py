import mysql.connector
import requests
import os
import shutil
import uuid
from typing import List, Optional
import sys
from app.config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, SHOPIFY_ACCESS_TOKEN
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Body, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="Floorplan Recognition API")

# Add floorplan module to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Initialize scheduler
scheduler = BackgroundScheduler()

db_connection = None


def get_db_connection():
    global db_connection
    if db_connection is None or db_connection.close:
        try:
            db_connection = mysql.connector.connect(
                host=DB_SERVER, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
            )
        except Exception as e:
            print(f"Failed to connect to database: {e}")
    return db_connection


def get_products_data():
    # Shopify credentials and store details
    SHOPIFY_STORE = "https://mall.aroomy.com"

    # GraphQL query to get the product listings from the "Featured" collection
    query = """
    {
      collectionByHandle(handle: "featured") {
        title
        products(first: 10) {
          edges {
            node {
              title
              description
              onlineStoreUrl
              priceRange {
                minVariantPrice {
                  amount
                }
              }
              images(first: 5) {
                edges {
                  node {
                    originalSrc
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    # API request to Shopify
    url = f"{SHOPIFY_STORE}/api/2024-01/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }
    response = requests.post(url, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()["data"]["collectionByHandle"]["products"]["edges"]

    raise Exception(f"Failed to retrieve products. Status code: {response.status_code}")


# Create necessary directories
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "output")

# Ensure directories exist
for directory in [UPLOAD_DIR, PROCESSED_DIR, OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)


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


# Import floor plan processing functions
from floorplan.preprocess import preprocess_image
# Use detection factory to automatically switch between real and mock implementations
from floorplan.mock_detection import load_model, detect_objects

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
    return {"status": "UP"}


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
