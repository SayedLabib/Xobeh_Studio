from pydantic import BaseModel, Field


class GeminiImageRequest(BaseModel):
    """Request schema for Gemini image generation"""
    prompt: str = Field(
        ..., 
        description="Text prompt describing the image to generate",
        min_length=1,
        max_length=1000,
        example="A beautiful chocolate lady dancing in the kitchen"
    )


class GeminiImageResponse(BaseModel):
    """Response schema for Gemini image generation"""
    success: bool = Field(description="Whether the generation was successful")
    message: str = Field(description="Status message")
    image_url: str = Field(description="URL to the generated image")


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str = Field(description="Error message")