import os
import logging
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiService:
    """Service for handling Google Gemini Vision API interactions."""
    
    def __init__(self):
        """Initialize the Gemini service with API key."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
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
            
            # Convert image bytes to PIL Image for the API
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            # Generate content using the correct API
            response = self.model.generate_content(
                [prompt, image],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )
            
            self.logger.info(f"API Response received")
            
            # Extract text from response
            if response and response.text:
                caption_text = response.text.strip()
            else:
                raise ValueError("No response text from Gemini API")
            
            self.logger.info(f"Successfully generated caption: {caption_text[:50]}...")
            
            return caption_text
            
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
            
            # Convert image bytes to PIL Image for the API
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            response = self.model.generate_content([prompt, image])
            
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
    
    def identify_location(self, image_bytes: bytes) -> dict:
        """
        Identify and analyze the location/setting in the image.
        
        Args:
            image_bytes: Image data in bytes format
            
        Returns:
            Dictionary containing location analysis
        """
        try:
            prompt = (
                "Analyze this image and identify the location/setting with as much detail as possible. "
                "Please provide:\n\n"
                "1. **Location Type**: (Indoor/Outdoor, specific type like restaurant, park, office, etc.)\n"
                "2. **Geographic Clues**: Any visible signs, architecture, or cultural indicators that might suggest a region or country\n"
                "3. **Specific Details**: Street names, building names, landmarks, or any readable text\n"
                "4. **Environmental Context**: Weather, time of day, season if determinable\n"
                "5. **Architectural Style**: Building design, materials, cultural architectural elements\n"
                "6. **Background Elements**: What's visible in the background that provides location context\n"
                "7. **Confidence Level**: How certain you are about the location identification (High/Medium/Low)\n\n"
                "If this appears to be a famous landmark or recognizable location, please identify it specifically. "
                "Look for any text, signs, or distinctive features that could help pinpoint the exact location."
            )
            
            # Convert image bytes to PIL Image for the API
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            response = self.model.generate_content([prompt, image])
            
            return {
                "location_analysis": response.text if response.text else "No location analysis available",
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error identifying location: {str(e)}")
            return {
                "location_analysis": f"Location analysis failed: {str(e)}",
                "success": False
            }
    
    def identify_product(self, image_bytes: bytes) -> dict:
        """
        Identify and analyze products in the image (especially for e-commerce).
        
        Args:
            image_bytes: Image data in bytes format
            
        Returns:
            Dictionary containing product analysis
        """
        try:
            prompt = (
                "Analyze this image for any products, items, or objects that could be commercial/retail items. "
                "Please provide detailed information:\n\n"
                "1. **Product Identification**: What specific products/items do you see?\n"
                "2. **Brand Recognition**: Any visible brand names, logos, or trademarks\n"
                "3. **Product Category**: What category does each item belong to (electronics, clothing, food, etc.)\n"
                "4. **Product Details**: \n"
                "   - Model numbers or product codes if visible\n"
                "   - Size, color, material descriptions\n"
                "   - Condition (new, used, packaging status)\n"
                "5. **Text Analysis**: Any readable text on products, labels, tags, or packaging\n"
                "6. **Price Information**: Any visible price tags or pricing information\n"
                "7. **Product Context**: Is this a retail display, personal item, advertisement, etc.?\n"
                "8. **Quality Assessment**: Product condition, authenticity indicators\n"
                "9. **Comparable Products**: Similar items or alternatives you can identify\n"
                "10. **Market Context**: Estimated value range or market category (luxury, budget, mid-range)\n\n"
                "If multiple products are visible, analyze each one separately. "
                "Pay special attention to any barcodes, QR codes, or product identifiers."
            )
            
            # Convert image bytes to PIL Image for the API
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            response = self.model.generate_content([prompt, image])
            
            return {
                "product_analysis": response.text if response.text else "No product analysis available",
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error identifying product: {str(e)}")
            return {
                "product_analysis": f"Product analysis failed: {str(e)}",
                "success": False
            }
    
    def comprehensive_analysis(self, image_bytes: bytes) -> dict:
        """
        Perform comprehensive analysis combining location, product, and general analysis.
        
        Args:
            image_bytes: Image data in bytes format
            
        Returns:
            Dictionary containing comprehensive analysis
        """
        try:
            prompt = (
                "Perform a comprehensive analysis of this image. I need you to be a detective and provide "
                "extremely detailed information about everything you can observe:\n\n"
                
                "**LOCATION & SETTING ANALYSIS:**\n"
                "- Identify the specific location type and setting\n"
                "- Look for geographic, cultural, or architectural clues\n"
                "- Identify any landmarks, street signs, or location indicators\n"
                "- Analyze the environment (indoor/outdoor, weather, time of day)\n\n"
                
                "**PRODUCT & OBJECT IDENTIFICATION:**\n"
                "- Identify all products, brands, and commercial items\n"
                "- Read and transcribe any visible text, labels, or signs\n"
                "- Analyze product categories, conditions, and market positioning\n"
                "- Look for barcodes, model numbers, or product identifiers\n\n"
                
                "**CONTEXTUAL ANALYSIS:**\n"
                "- What is the purpose/context of this image?\n"
                "- Is this commercial, personal, documentary, or artistic?\n"
                "- What story does this image tell?\n"
                "- Any cultural, social, or economic indicators?\n\n"
                
                "**TECHNICAL DETAILS:**\n"
                "- Photography style and quality\n"
                "- Lighting conditions and camera angle\n"
                "- Image composition and focus points\n\n"
                
                "**SPECIFIC IDENTIFICATIONS:**\n"
                "- Any recognizable people, places, or things\n"
                "- Specific brand names, product models, or locations\n"
                "- Any unique or distinctive features\n\n"
                
                "Please be as specific and detailed as possible. If you're uncertain about something, "
                "indicate your confidence level and provide your best analysis based on visual evidence."
            )
            
            # Convert image bytes to PIL Image for the API
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            response = self.model.generate_content([prompt, image])
            
            return {
                "comprehensive_analysis": response.text if response.text else "No comprehensive analysis available",
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive analysis: {str(e)}")
            return {
                "comprehensive_analysis": f"Comprehensive analysis failed: {str(e)}",
                "success": False
            }
    
    def extract_text_and_details(self, image_bytes: bytes) -> dict:
        """
        Extract and analyze all visible text and readable details in the image.
        
        Args:
            image_bytes: Image data in bytes format
            
        Returns:
            Dictionary containing text extraction results
        """
        try:
            prompt = (
                "Extract and analyze ALL visible text and readable details in this image. "
                "Please provide:\n\n"
                
                "**TEXT EXTRACTION:**\n"
                "- All readable text (signs, labels, documents, screens, etc.)\n"
                "- Text language identification\n"
                "- Text context and meaning\n\n"
                
                "**NUMBERS & CODES:**\n"
                "- Phone numbers, addresses, postal codes\n"
                "- Product codes, model numbers, serial numbers\n"
                "- Prices, measurements, quantities\n"
                "- Dates and times\n\n"
                
                "**IDENTIFIABLE INFORMATION:**\n"
                "- Brand names and logos\n"
                "- Company names and business information\n"
                "- Website URLs or social media handles\n"
                "- Any contact information\n\n"
                
                "**LOCATION INDICATORS:**\n"
                "- Street names and addresses\n"
                "- City, state, or country names\n"
                "- Landmark or building names\n"
                "- Directional signs or maps\n\n"
                
                "**PRODUCT INFORMATION:**\n"
                "- Product names and descriptions\n"
                "- Ingredient lists or specifications\n"
                "- Usage instructions or warnings\n"
                "- Certification marks or quality indicators\n\n"
                
                "Please transcribe text exactly as it appears and provide context for each piece of information."
            )
            
            # Convert image bytes to PIL Image for the API
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            response = self.model.generate_content([prompt, image])
            
            return {
                "text_analysis": response.text if response.text else "No text analysis available",
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting text: {str(e)}")
            return {
                "text_analysis": f"Text analysis failed: {str(e)}",
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
            response = self.model.generate_content("Hello, this is a test.")
            return response.text is not None
            
        except Exception as e:
            self.logger.error(f"API key validation failed: {str(e)}")
            return False
