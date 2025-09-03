from pydantic import BaseModel, Field
from typing import Optional


class StableDiffusionRequest(BaseModel):
    """Request schema for Stable Diffusion image generation"""
    prompt: str = Field(
        ..., 
        description="Text prompt describing the image to generate",
        min_length=1,
        max_length=1000,
        example="A beautiful landscape with mountains and a lake at sunset"
    )


class StableDiffusionResponse(BaseModel):
    """Response schema for Stable Diffusion image generation"""
    success: bool = Field(description="Whether the generation was successful")
    message: str = Field(description="Status message")
    image_url: str = Field(description="URL to the generated image")


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str = Field(description="Error message")