import os
import logging
from typing import Optional
from google import genai
from google.genai import types

class GeminiService:
    """Service for handling Google Gemini Vision API interactions."""
    
    def __init__(self):
        """Initialize the Gemini service with API key."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def generate_caption(
        self, 
        image_bytes: bytes, 
        style: str = "descriptive",
        max_tokens: int = 150,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a caption for the given image using Gemini Vision API.
        
        Args:
            image_bytes: Image data in bytes format
            style: Caption style (descriptive, creative, technical, simple)
            max_tokens: Maximum number of tokens in the response
            temperature: Creativity level (0.0 to 1.0)
            
        Returns:
            Generated caption as string
            
        Raises:
            Exception: If caption generation fails
        """
        try:
            # Create style-specific prompts
            style_prompts = {
                "descriptive": (
                    "Provide a detailed, descriptive caption for this image. "
                    "Include information about objects, people, setting, colors, "
                    "composition, and mood. Be specific and informative."
                ),
                "creative": (
                    "Create an imaginative and creative caption for this image. "
                    "Use vivid language, metaphors, and storytelling elements. "
                    "Make it engaging and artistic."
                ),
                "technical": (
                    "Provide a technical analysis of this image. "
                    "Include details about composition, lighting, photography "
                    "techniques, visual elements, and technical aspects."
                ),
                "simple": (
                    "Provide a simple, clear caption for this image in one "
                    "or two sentences. Focus on the main subject and key elements."
                )
            }
            
            prompt = style_prompts.get(style, style_prompts["descriptive"])
            
            self.logger.info(f"Generating {style} caption with temperature {temperature}")
            
            # Generate content using Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            if not response.text:
                raise ValueError("Empty response from Gemini API")
            
            caption = response.text.strip()
            self.logger.info(f"Successfully generated caption: {caption[:50]}...")
            
            return caption
            
        except Exception as e:
            self.logger.error(f"Error generating caption: {str(e)}")
            raise Exception(f"Failed to generate caption: {str(e)}")
    
    def analyze_image_content(self, image_bytes: bytes) -> dict:
        """
        Analyze image content for additional metadata.
        
        Args:
            image_bytes: Image data in bytes format
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            prompt = (
                "Analyze this image and provide the following information in a "
                "structured format:\n"
                "1. Main subjects/objects\n"
                "2. Setting/location\n"
                "3. Colors and lighting\n"
                "4. Mood/atmosphere\n"
                "5. Notable features\n"
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                    prompt
                ]
            )
            
            return {
                "analysis": response.text if response.text else "No analysis available",
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing image: {str(e)}")
            return {
                "analysis": f"Analysis failed: {str(e)}",
                "success": False
            }
    
    def validate_api_key(self) -> bool:
        """
        Validate if the API key is working.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Test with a simple text generation
            response = self.client.models.generate_content(
                model=self.model,
                contents="Hello, this is a test."
            )
            return response.text is not None
            
        except Exception as e:
            self.logger.error(f"API key validation failed: {str(e)}")
            return False
