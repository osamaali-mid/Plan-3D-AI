import os
from typing import Dict, Any, Optional
import json
import uuid
from datetime import datetime
from .openai_client import OpenAIClient
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "carpet_output")
class CarpetGenerationService:
    """Service for carpet design generation using OpenAI APIs"""
    
    # Standard system prompt to combine with user input
    DEFAULT_SYSTEM_PROMPT = """
    You are a specialized AI for generating beautiful carpet designs. 
    Take the user's input and convert it into a detailed and clear prompt for generating carpet images.
    Focus on patterns, colors, textures, and styles that would make an attractive carpet.
    Include details about:
    - Pattern type (geometric, floral, abstract, etc.)
    - Color scheme and specific colors
    - Texture description (plush, flat weave, shaggy, etc.)
    - Style influence (modern, traditional, vintage, minimalist, etc.)
    - Material impression (wool, silk, synthetic, etc.)
    
    Your output should be a refined, detailed description that will help generate a realistic and attractive carpet design.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the carpet generation service"""
        self.openai_client = OpenAIClient(api_key=openai_api_key)
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                       "data", "carpet_output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_carpet(self, 
                        user_prompt: str, 
                        system_prompt: Optional[str] = None,
                        reference_gpt: Optional[bool] = False,
                        size: str = "1024x1024") -> Dict[str, Any]:
        """
        Generate a carpet design based on user prompt
        
        Args:
            user_prompt: User's description of desired carpet
            system_prompt: Optional custom system prompt 
            reference_image_path: Optional path to a reference image
            size: Size of the image to generate
            
        Returns:
            Dictionary with generation results including image URLs and metadata
        """
        try:
            # Use default system prompt if none provided
            if not system_prompt:
                system_prompt = self.DEFAULT_SYSTEM_PROMPT
                
            # Enhance user prompt with GPT-4 if a reference image is provided
            if reference_gpt:
                carpet_id = str(uuid.uuid4())
                timestamp = datetime.now().isoformat()
                
                image_bytes = self.openai_client.generate_carpet_with_gpt(
                  prompt=user_prompt,
                  size=size
                )
                
                image_path = os.path.join(self.output_dir, f"{carpet_id}.png")
                with open(image_path, "wb") as f:
                  f.write(image_bytes)
                
                result = {
                    "id": carpet_id,
                    "timestamp": timestamp,
                    "original_prompt": user_prompt,
                    "image_urls": [f"/api/carpet/images/{carpet_id}.png"],
                    "size": size
                }
                
                metadata_path = os.path.join(self.output_dir, f"{carpet_id}_metadata.json")
                with open(metadata_path, "w") as f:
                    json.dump(result, f, indent=2)
                
                return result
            else:
                # Generate the carpet image using DALL-E 3
                generation_result = self.openai_client.generate_carpet_with_dalle(
                    prompt=user_prompt,
                    size=size
                )
            
            # Prepare the result with metadata
            result = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "original_prompt": user_prompt,
                "image_urls": [data["url"] for data in generation_result["data"]],
                "size": size
            }
            
            # Save result metadata for future reference
            metadata_path = os.path.join(self.output_dir, f"{result['id']}_metadata.json")
            with open(metadata_path, "w") as f:
                json.dump(result, f, indent=2)
                
            return result
            
        except Exception as e:
            # Log the error and re-raise
            print(f"Error generating carpet: {str(e)}")
            raise
