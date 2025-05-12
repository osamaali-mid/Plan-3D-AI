from pydantic import BaseModel
from typing import List, Optional

class CarpetPromptRequest(BaseModel):
    prompt: str
    custom_system_prompt: Optional[str] = None
    size: str = "1024x1024"

class CarpetGenerationResponse(BaseModel):
    id: str
    timestamp: str
    original_prompt: str
    image_urls: List[str]
    size: str
