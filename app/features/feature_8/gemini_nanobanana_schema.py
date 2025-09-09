from pydantic import BaseModel, Field


class GeminiNanoBananaRequest(BaseModel):
    """Request schema for Gemini NanoBanana image generation using streaming API"""
    prompt: str = Field(
        description="Text prompt describing the banana costume image to generate",
        min_length=1,
        max_length=1000,
        example="Generate an image of a banana wearing a superhero costume."
    )


class GeminiNanoBananaResponse(BaseModel):
    """Response schema for Gemini NanoBanana image generation"""
    success: bool = Field(description="Whether the generation was successful")
    message: str = Field(description="Status message")
    image_url: str = Field(description="URL to the generated banana costume image")
    filename: str = Field(description="Generated filename")


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str = Field(description="Error message")