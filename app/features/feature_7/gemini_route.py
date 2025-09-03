from fastapi import APIRouter, HTTPException
import logging

from .gemini_schema import GeminiImageRequest, GeminiImageResponse, ErrorResponse
from .gemini_service import gemini_service

# Setup logging
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(
    prefix="/nano-banana",
    tags=["Gemini Image Generation"]
)


@router.post("/generate", response_model=GeminiImageResponse)
async def generate_image(request: GeminiImageRequest):
    """
    Generate an image from a text prompt using Google's Gemini Imagen model
    
    Takes a text prompt and returns a URL to the generated image.
    Uses Gemini's imagen-4.0-generate-001 model with predefined settings.
    """
    try:
        logger.info(f"Generating image with Gemini for prompt: {request.prompt[:50]}...")
        
        # Generate the image
        filename, image_url = gemini_service.generate_image(request.prompt)
        
        return GeminiImageResponse(
            success=True,
            message="Image generated successfully with Gemini",
            image_url=image_url
        )
        
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(
            status_code=500,
            detail=f"Service configuration error: {str(ve)}"
        )
        
    except Exception as e:
        logger.error(f"Error in Gemini image generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate image: {str(e)}"
        )