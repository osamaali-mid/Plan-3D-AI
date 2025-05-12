import os
import base64
from typing import Optional, Dict, Any
from openai import OpenAI

class OpenAIClient:
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI client with API key"""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Provide it as an argument or set OPENAI_API_KEY environment variable.")
        
        # Initialize the official OpenAI client
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_carpet_with_dalle(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """
        Generate carpet design using DALL-E 3
        
        Args:
            prompt: User prompt for carpet generation
            size: Size of the image (1024x1024, 1024x1792, or 1792x1024)
            n: Number of images to generate (1-10)
            
        Returns:
            Dictionary with generation results compatible with the original implementation
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="hd",
                response_format="url"
            )
            
            # Convert to dictionary compatible with the original implementation
            result = {
                "created": response.created,
                "data": []
            }
            
            for image in response.data:
                result["data"].append({
                    "url": image.url,
                    "revised_prompt": getattr(image, "revised_prompt", prompt)
                })
                
            return result
            
        except Exception as e:
            raise Exception(f"DALL-E API error: {str(e)}")
        
    def generate_carpet_with_gpt(self,  prompt: str, size: str = "1024x1024",) -> bytes:
        """
        Use GPT-IMAGE-1
        
        Args:
            prompt: User's request/prompt
            image_data: Optional base64-encoded image data
            
        Returns:
            Dictionary with GPT response compatible with the original implementation
        """
        try:
            
            response = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size,
            )
            
            image_base64 = response.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
                
            return image_bytes
            
        except Exception as e:
            raise Exception(f"GPT IMAGE 1 API error: {str(e)}")
    
