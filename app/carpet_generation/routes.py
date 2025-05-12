import os
import json
from fastapi import APIRouter, HTTPException

from ..config import OPENAI_API_KEY
from .schemas import CarpetPromptRequest, CarpetGenerationResponse
from .service import CarpetGenerationService

# Initialize the router
router = APIRouter(prefix="/api/carpet", tags=["carpet"])

# Initialize carpet generation service
carpet_service = CarpetGenerationService(openai_api_key=OPENAI_API_KEY)

@router.post("/generate", response_model=CarpetGenerationResponse)
async def generate_carpet(request: CarpetPromptRequest):
    """Generate a carpet design based on text prompt"""
    try:
        # Generate the carpet design
        result = carpet_service.generate_carpet(
            user_prompt=request.prompt,
            system_prompt=request.custom_system_prompt,
            size=request.size
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating carpet design: {str(e)}")


@router.post("/generate-with-gpt")
async def generate_carpet_with_gpt(request: CarpetPromptRequest):
    """Generate a carpet design based on text prompt and a reference image"""
    try:
        # Generate the carpet design
        result = carpet_service.generate_carpet(
            user_prompt=request.prompt,
            reference_gpt=True,
            size=request.size
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating carpet design: {str(e)}")


@router.get("/results/{result_id}")
def get_carpet_result(result_id: str):
    """Get metadata for a specific carpet generation"""
    metadata_file = os.path.join(carpet_service.output_dir, f"{result_id}_metadata.json")
    
    if not os.path.exists(metadata_file):
        raise HTTPException(status_code=404, detail="Carpet generation result not found")
    
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    
    return metadata

@router.get("/results")
def get_carpet_results():
    """Get all carpet generation metadata"""
    try:
        metadata_files = []

        for f in os.listdir(carpet_service.output_dir):
          if f.endswith("_metadata.json"):
            metadata_files.append(f)
        
        if not metadata_files:
            return {"results": []}
        print(metadata_files, 'metadata_files')
        results = []
        for file_name in metadata_files:
            file_path = os.path.join(carpet_service.output_dir, file_name)
            with open(file_path, "r") as f:
                metadata = json.load(f)
                results.append(metadata)
        
        results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return {"results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving carpet results: {str(e)}")