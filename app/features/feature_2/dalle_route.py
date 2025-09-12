from fastapi import APIRouter, HTTPException
from .dalle_schema import DalleRequest, DalleResponse
from .dalle_service import DalleService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["dalle"], prefix="/dalle")
dalle_service = DalleService()

@router.post("/generate", response_model=DalleResponse)
async def generate_image(request: DalleRequest):
    """
    Generate an image using DALL-E 3
    """
    try:
        image_url = await dalle_service.generate_image(request.prompt)
        return DalleResponse(image_url=image_url)
        
    except Exception as e:
        logger.error(f"Error in image generation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
