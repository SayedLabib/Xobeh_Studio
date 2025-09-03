import torch
import base64
import io
import time
import logging
import os
import uuid
from PIL import Image
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from typing import Optional, Tuple
import gc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StableDiffusionService:
    """Service class for handling Stable Diffusion image generation"""
    
    def __init__(self):
        self.pipeline = None
        self.model_id = os.getenv("MODEL_ID", "runwayml/stable-diffusion-v1-5")
        self.device = self._get_device()
        self.images_dir = os.getenv("IMAGES_DIR", "generated_images")
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")
        
        # Create images directory if it doesn't exist
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Load default generation parameters from environment
        self.default_negative_prompt = os.getenv("NEGATIVE_PROMPT", "blurry, low quality, distorted, deformed")
        self.default_width = int(os.getenv("IMAGE_WIDTH", "512"))
        self.default_height = int(os.getenv("IMAGE_HEIGHT", "512"))
        self.default_steps = int(os.getenv("NUM_INFERENCE_STEPS", "50"))
        self.default_guidance = float(os.getenv("GUIDANCE_SCALE", "7.5"))
        self.default_seed = os.getenv("SEED", None)
        if self.default_seed and self.default_seed.lower() != "none":
            self.default_seed = int(self.default_seed)
        else:
            self.default_seed = None
            
        self._initialize_pipeline()
    
    def _get_device(self) -> str:
        """Force CPU usage"""
        return "cpu"
    
    def _initialize_pipeline(self):
        """Initialize the Stable Diffusion pipeline for CPU"""
        try:
            logger.info(f"Loading Stable Diffusion model: {self.model_id}")
            logger.info(f"Using device: {self.device}")
            
            # Load the pipeline with CPU-optimized settings
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32,  # Use float32 for CPU
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Use DPM Solver for faster inference
            self.pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipeline.scheduler.config
            )
            
            # Move to CPU device
            self.pipeline = self.pipeline.to(self.device)
            
            logger.info("Pipeline initialized successfully on CPU")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {str(e)}")
            raise e
    
    def generate_image(self, prompt: str) -> Tuple[str, str]:
        """
        Generate an image using Stable Diffusion on CPU
        
        Args:
            prompt: Text description of the desired image
            
        Returns:
            Tuple of (image_filename, image_url)
        """
        try:
            start_time = time.time()
            logger.info(f"Generating image for prompt: {prompt[:50]}...")
            
            # Enhance the prompt for better quality
            enhanced_prompt = self.enhance_prompt(prompt)
            
            # Set seed for reproducibility if specified
            if self.default_seed is not None:
                torch.manual_seed(self.default_seed)
            
            # Generate the image using environment defaults
            result = self.pipeline(
                prompt=enhanced_prompt,
                negative_prompt=self.default_negative_prompt,
                width=self.default_width,
                height=self.default_height,
                num_inference_steps=self.default_steps,
                guidance_scale=self.default_guidance,
                generator=torch.Generator().manual_seed(self.default_seed) if self.default_seed else None
            )
            
            # Clean up memory
            gc.collect()
            
            generation_time = time.time() - start_time
            logger.info(f"Image generated in {generation_time:.2f} seconds")
            
            # Save image to file
            image = result.images[0]
            filename = f"{uuid.uuid4()}.png"
            filepath = os.path.join(self.images_dir, filename)
            image.save(filepath)
            
            # Create image URL
            image_url = f"{self.base_url}/images/{filename}"
            
            return filename, image_url
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise e
    
    def enhance_prompt(self, user_prompt: str) -> str:
        """
        Enhance user prompt with quality and style modifiers
        
        Args:
            user_prompt: Original user prompt
            
        Returns:
            Enhanced prompt with quality modifiers
        """
        quality_modifiers = [
            "highly detailed",
            "professional photography",
            "8k resolution",
            "masterpiece",
            "best quality",
            "sharp focus"
        ]
        
        enhanced_prompt = f"{user_prompt}, {', '.join(quality_modifiers)}"
        return enhanced_prompt
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            "model_id": self.model_id,
            "device": self.device,
            "pipeline_type": "StableDiffusionPipeline",
            "scheduler": self.pipeline.scheduler.__class__.__name__ if self.pipeline else None,
            "torch_dtype": str(self.pipeline.unet.dtype) if self.pipeline else None,
            "default_settings": {
                "width": self.default_width,
                "height": self.default_height,
                "steps": self.default_steps,
                "guidance_scale": self.default_guidance,
                "seed": self.default_seed
            }
        }
    
    def cleanup(self):
        """Clean up resources"""
        if self.pipeline:
            del self.pipeline
            self.pipeline = None
        
        gc.collect()
        logger.info("Resources cleaned up")


# Global service instance
stable_diffusion_service = StableDiffusionService()