from fastapi import APIRouter, HTTPException
import logging

from .stable_diffusion_schema import StableDiffusionRequest, StableDiffusionResponse
from .stable_diffusion_service import stable_diffusion_service

# Setup logging
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(
    prefix="/stable-diffusion",
    tags=["Stable Diffusion"]
)


@router.post("/generate", response_model=StableDiffusionResponse)
async def generate_image(request: StableDiffusionRequest):
    """
    Generate an image from a text prompt using Stable Diffusion
    
    Takes a text prompt and returns a URL to the generated image.
    All generation settings are configured via environment variables.
    """
    try:
        logger.info(f"Generating image for prompt: {request.prompt[:50]}...")
        
        # Generate the image
        filename, image_url = stable_diffusion_service.generate_image(request.prompt)
        
        return StableDiffusionResponse(
            success=True,
            message="Image generated successfully",
            image_url=image_url
        )
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate image: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Check if the Stable Diffusion service is ready"""
    try:
        is_ready = stable_diffusion_service.pipeline is not None
        
        return {
            "status": "ready" if is_ready else "loading",
            "message": "Service is ready" if is_ready else "Model is loading...",
            "model": stable_diffusion_service.model_id,
            "device": stable_diffusion_service.device
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Service error: {str(e)}"
        }


@router.get("/info")
async def get_model_info():
    """Get information about the loaded model and settings"""
    try:
        model_info = stable_diffusion_service.get_model_info()
        return {
            "success": True,
            "model_info": model_info
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model info: {str(e)}"
        )