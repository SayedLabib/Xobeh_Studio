from fastapi import APIRouter, HTTPException, Query

from .gemini_nanobanana_schema import GeminiNanoBananaRequest, GeminiNanoBananaResponse, StyleEnum, ShapeEnum
from .gemini_nanobanana_service import gemini_nanobanana_service

router = APIRouter(
    prefix="/nanobanana",
    tags=["Gemini NanoBanana"]
)


@router.post("/generate", response_model=GeminiNanoBananaResponse)
async def generate_banana_costume(
    request: GeminiNanoBananaRequest,
    style: str = Query(..., description="Image style: Photo, Illustration, Comic, Anime, Abstract, Fantasy, PopArt"),
    shape: str = Query(..., description="Image shape: square, portrait, landscape")
):
    """
    Generate a banana costume image using Gemini NanoBanana with specified style and shape
    """
    try:
        # Validate style parameter
        valid_styles = ["Photo", "Illustration", "Comic", "Anime", "Abstract", "Fantasy", "PopArt"]
        if style not in valid_styles:
            raise HTTPException(status_code=400, detail=f"Invalid style. Must be one of: {', '.join(valid_styles)}")
        
        # Validate shape parameter
        valid_shapes = ["square", "portrait", "landscape"]
        if shape not in valid_shapes:
            raise HTTPException(status_code=400, detail=f"Invalid shape. Must be one of: {', '.join(valid_shapes)}")
        
        filename, image_url = gemini_nanobanana_service.generate_banana_costume_image(
            prompt=request.prompt,
            style=style,
            shape=shape
        )
        
        success_message = f"Successfully generated {style} style banana costume image in {shape} format using Gemini NanoBanana"
        
        return GeminiNanoBananaResponse(
            success=True,
            success_message=success_message,
            image_url=image_url,
            filename=filename,
            shape=shape
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))