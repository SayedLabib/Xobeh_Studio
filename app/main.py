from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os
import sys

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import feature routes directly
from features.feature_2.dalle_route import router as dalle_router
from features.feature_4.videogen_route import router as videogen_router
from features.feature_5.prompt_enhancer_route import router as prompt_enhancer_router
# from features.feature_6.stable_diffusion_route import router as stable_diffusion_router
from features.feature_7.gemini_route import router as gemini_router
from features.feature_8.gemini_nanobanana_route import router as gemini_nanobanana_router
from features.feature_9.flux_kontext_dev_route import router as flux_kontext_dev_router
from features.feature_10.videogen3_route import router as videogen3_router
from features.feature_11.flux_kontext_dev_edit_route import router as flux_kontext_edit_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="XobehStudio AI Services",
    description="AI service platform with Stable Diffusion image generation, Gemini AI, and intelligent prompt enhancement",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving generated images
images_dir = os.path.join(os.path.dirname(__file__), "..", "generated_images")
os.makedirs(images_dir, exist_ok=True)
app.mount("/images", StaticFiles(directory=images_dir), name="images")

# Include routers
app.include_router(prompt_enhancer_router, prefix="/api/v1")
app.include_router(dalle_router, prefix="/api/v1")
app.include_router(videogen_router, prefix="/api/v1")
app.include_router(videogen3_router, prefix="/api/v1")
app.include_router(gemini_router, prefix="/api/v1")
app.include_router(gemini_nanobanana_router, prefix="/api/v1")
app.include_router(flux_kontext_dev_router, prefix="/api/v1")
app.include_router(flux_kontext_edit_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "XobehStudio AI Services",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """General health check endpoint"""
    return {
        "status": "healthy",
        "message": "XobehStudio AI Services is running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )