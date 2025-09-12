from pydantic import BaseModel

class DalleRequest(BaseModel):
    """Schema for DALL-E image generation request"""
    prompt: str

class DalleResponse(BaseModel):
    """Schema for DALL-E image generation response"""
    image_url: str
