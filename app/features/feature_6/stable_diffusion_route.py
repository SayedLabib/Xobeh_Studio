from fastapi import APIRouter, HTTPException
import logging

from .stable_diffusion_schema import StableDiffusionRequest, StableDiffusionResponse
from .stable_diffusion_service import stable_diffusion_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/stable-diffusion",
    tags=["Stable Diffusion"]
)


@router.post("/generate", response_model=StableDiffusionResponse)
async def generate_image(request: StableDiffusionRequest):
    """Generate an image from a text prompt using Stable Diffusion"""
    try:
        logger.info(f"Generating image: {request.prompt[:50]}...")
        
        filename, image_url = stable_diffusion_service.generate_image(request.prompt)
        
        return StableDiffusionResponse(
            success=True,
            message="Image generated successfully",
            image_url=image_url
        )
        
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate image: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Check service status"""
    try:
        info = stable_diffusion_service.get_info()
        
        return {
            "status": "ready" if info["is_ready"] else "loading",
            "message": "Service is ready" if info["is_ready"] else "Loading model...",
            "model": info["model_id"],
            "device": info["device"]
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "message": f"Service error: {str(e)}"
        }


@router.get("/info")
async def get_info():
    """Get service information"""
    try:
        info = stable_diffusion_service.get_info()
        return {"success": True, "info": info}
        
    except Exception as e:
        logger.error(f"Info request failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get info: {str(e)}"
        )


@router.post("/cleanup")
async def cleanup():
    """Clean up resources"""
    try:
        stable_diffusion_service.cleanup()
        return {"success": True, "message": "Resources cleaned up"}
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Cleanup failed: {str(e)}"
        )