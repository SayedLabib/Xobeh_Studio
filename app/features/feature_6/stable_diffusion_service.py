import torch
import os
import uuid
import time
import logging
from diffusers import StableDiffusion3Pipeline, BitsAndBytesConfig, SD3Transformer2DModel
from typing import Tuple
import gc
import sys

# Add the app directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.config import config

logger = logging.getLogger(__name__)


class StableDiffusionService:
    """Stable Diffusion 3.5 Large service"""
    
    def __init__(self):
        self.pipeline = None
        self.model_id = config.STABLE_DIFFUSION_MODEL_ID
        self.local_model_path = "models/stable-diffusion-3.5-large"
        self.device = self._get_device()
        self.images_dir = config.IMAGES_DIR
        self.base_url = config.BASE_URL
        self.hf_token = config.HUGGINGFACE_TOKEN
        
        # Create images directory
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Generation settings
        self.width = config.IMAGE_WIDTH
        self.height = config.IMAGE_HEIGHT
        self.steps = config.NUM_INFERENCE_STEPS
        self.guidance = config.GUIDANCE_SCALE
        self.negative_prompt = config.NEGATIVE_PROMPT
        self.max_sequence_length = 256
        
        # Load model immediately
        self._load_pipeline()
    
    def is_model_downloaded(self) -> bool:
        """Check if model is available locally"""
        return os.path.exists(self.local_model_path) and os.path.exists(os.path.join(self.local_model_path, "model_index.json"))
    
    def _get_device(self) -> str:
        """Get the best available device"""
        if torch.cuda.is_available():
            device = "cuda:0"
            logger.info(f"CUDA Available: {torch.cuda.is_available()}")
            logger.info(f"CUDA Device: {torch.cuda.get_device_name(0)}")
            logger.info(f"CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return device
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            logger.info("Using MPS (Apple Silicon)")
            return "mps"
        else:
            logger.warning("CUDA not available, falling back to CPU")
            return "cpu"
    
    def _load_pipeline(self):
        """Load Stable Diffusion 3.5 Large from local storage or HuggingFace"""
        try:
            # Determine model source
            if os.path.exists(self.local_model_path):
                logger.info(f"Loading from local storage: {self.local_model_path}")
                model_source = self.local_model_path
                use_token = False
            else:
                logger.info(f"Loading from HuggingFace: {self.model_id}")
                model_source = self.model_id
                use_token = True
                if not self.hf_token:
                    raise ValueError("HuggingFace token required. Set HUGGINGFACE_TOKEN in .env")
            
            logger.info(f"Device: {self.device}")
            
            if self.device.startswith("cuda"):
                torch.set_float32_matmul_precision('high')
                logger.info("TensorFloat-32 enabled")
                
                # 4-bit quantization config
                nf4_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16
                )
                
                # Load transformer
                transformer_kwargs = {
                    "subfolder": "transformer",
                    "quantization_config": nf4_config,
                    "torch_dtype": torch.bfloat16,
                    "use_safetensors": True
                }
                if use_token:
                    transformer_kwargs["token"] = self.hf_token
                else:
                    transformer_kwargs["local_files_only"] = True
                
                model_nf4 = SD3Transformer2DModel.from_pretrained(model_source, **transformer_kwargs)
                
                # Load pipeline
                pipeline_kwargs = {
                    "transformer": model_nf4,
                    "torch_dtype": torch.bfloat16,
                    "use_safetensors": True
                }
                if use_token:
                    pipeline_kwargs["token"] = self.hf_token
                else:
                    pipeline_kwargs["local_files_only"] = True
                
                self.pipeline = StableDiffusion3Pipeline.from_pretrained(model_source, **pipeline_kwargs)
                self.pipeline.enable_model_cpu_offload()
                
            else:
                # CPU/MPS loading
                pipeline_kwargs = {
                    "torch_dtype": torch.float32 if self.device == "cpu" else torch.float16,
                    "use_safetensors": True
                }
                if use_token:
                    pipeline_kwargs["token"] = self.hf_token
                else:
                    pipeline_kwargs["local_files_only"] = True
                
                self.pipeline = StableDiffusion3Pipeline.from_pretrained(model_source, **pipeline_kwargs)
                self.pipeline = self.pipeline.to(self.device)
            
            logger.info("SD 3.5 Large loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load SD 3.5 Large: {e}")
            raise
    
    def generate_image(self, prompt: str) -> Tuple[str, str]:
        """Generate an image using Stable Diffusion 3.5 Large"""
        try:
            start_time = time.time()
            logger.info(f"Generating image: {prompt[:50]}")
            
            # Clear CUDA cache
            if self.device.startswith("cuda"):
                torch.cuda.empty_cache()
            
            # Generate image
            result = self.pipeline(
                prompt=prompt,
                negative_prompt=self.negative_prompt,
                width=self.width,
                height=self.height,
                num_inference_steps=self.steps,
                guidance_scale=self.guidance,
                max_sequence_length=self.max_sequence_length
            )
            
            # Save image
            image = result.images[0]
            filename = f"sd35_{uuid.uuid4().hex}.png"
            filepath = os.path.join(self.images_dir, filename)
            image.save(filepath, quality=95, optimize=True)
            
            # Create URL
            image_url = f"{self.base_url}/images/{filename}"
            
            # Cleanup
            if self.device.startswith("cuda"):
                torch.cuda.empty_cache()
            gc.collect()
            
            generation_time = time.time() - start_time
            logger.info(f"Image generated in {generation_time:.2f}s: {filename}")
            
            return filename, image_url
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            # Cleanup on error
            if self.device.startswith("cuda"):
                torch.cuda.empty_cache()
            gc.collect()
            raise
    
    def get_info(self) -> dict:
        """Get service information"""
        return {
            "model_id": self.model_id,
            "model_type": "Stable Diffusion 3.5 Large",
            "device": self.device,
            "is_ready": self.pipeline is not None,
            "model_downloaded": self.is_model_downloaded(),
            "local_model_path": self.local_model_path,
            "quantization": "4-bit NF4" if self.device.startswith("cuda") else "None",
            "settings": {
                "width": self.width,
                "height": self.height,
                "steps": self.steps,
                "guidance_scale": self.guidance,
                "max_sequence_length": self.max_sequence_length
            }
        }
    
    def cleanup(self):
        """Clean up resources"""
        if self.pipeline:
            del self.pipeline
            self.pipeline = None
        
        if self.device.startswith("cuda"):
            torch.cuda.empty_cache()
        
        gc.collect()
        logger.info("Resources cleaned up")


# Global service instance
stable_diffusion_service = StableDiffusionService()
