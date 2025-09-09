from fastapi import APIRouter, HTTPException

from .gemini_nanobanana_schema import GeminiNanoBananaRequest, GeminiNanoBananaResponse
from .gemini_nanobanana_service import gemini_nanobanana_service

router = APIRouter(
    prefix="/nanobanana",
    tags=["Gemini NanoBanana"]
)


@router.post("/generate", response_model=GeminiNanoBananaResponse)
async def generate_banana_costume(request: GeminiNanoBananaRequest):
    try:
        filename, image_url = gemini_nanobanana_service.generate_banana_costume_image(request.prompt)
        return GeminiNanoBananaResponse(
            success=True, 
            message="image generated successfully",
            image_url=image_url,
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))