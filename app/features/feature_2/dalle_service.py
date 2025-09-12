import logging
from openai import OpenAI
from core.config import config

logger = logging.getLogger(__name__)

class DalleService:
    """Service for generating images using DALL-E 3"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPEN_AI_API_KEY)
        
    async def generate_image(self, prompt: str) -> str:
        """
        Generate an image using DALL-E 3
        
        Args:
            prompt (str): The image description prompt
            
        Returns:
            str: URL of the generated image
        """
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="standard",
            )
            
            # Get the image URL from the response
            image_url = response.data[0].url
            
            logger.info(f"Successfully generated image for prompt: {prompt}")
            return image_url
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise
