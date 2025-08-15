"""
Chatbot service for interactive conversations about images using Gemini API.
"""

import os
import logging
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class ChatbotService:
    """Service for handling chatbot conversations with Gemini API."""
    
    def __init__(self):
        """Initialize the chatbot service with Gemini API client."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def chat_with_image(self, 
                       image_bytes: bytes, 
                       user_message: str,
                       chat_history: List[Dict[str, str]] = None) -> str:
        """
        Chat about an uploaded image with conversation history.
        
        Args:
            image_bytes: The image data as bytes
            user_message: User's question or message
            chat_history: Previous conversation history
            
        Returns:
            AI response as string
        """
        try:
            # Convert image bytes to PIL Image
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            # Build conversation context with history
            conversation_context = ""
            if chat_history:
                for message in chat_history[-5:]:  # Keep last 5 messages for context
                    role = "User" if message["role"] == "user" else "Assistant"
                    conversation_context += f"{role}: {message['content']}\n"
            
            # Create full prompt with context
            full_prompt = f"""You are a helpful AI assistant that can see and understand images. 
Provide detailed, accurate, and conversational responses about what you see. 
Be friendly and engaging while maintaining accuracy.

Previous conversation:
{conversation_context}

Current question: {user_message}"""
            
            response = self.model.generate_content(
                [full_prompt, image],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7
                )
            )
            
            if response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Error in chat_with_image: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def chat_without_image(self, 
                          user_message: str,
                          chat_history: List[Dict[str, str]] = None) -> str:
        """
        General chat without image context.
        
        Args:
            user_message: User's question or message
            chat_history: Previous conversation history
            
        Returns:
            AI response as string
        """
        try:
            # Build conversation context with history
            conversation_context = ""
            if chat_history:
                for message in chat_history[-5:]:  # Keep last 5 messages for context
                    role = "User" if message["role"] == "user" else "Assistant"
                    conversation_context += f"{role}: {message['content']}\n"
            
            # Create full prompt with context
            full_prompt = f"""You are Vispio's AI assistant, specialized in visual understanding and image analysis. 
While you can chat about general topics, your expertise is in helping users understand and describe visual content. 
Be helpful, friendly, and encourage users to upload images for visual analysis when relevant.

Previous conversation:
{conversation_context}

Current question: {user_message}"""
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=800,
                    temperature=0.7
                )
            )
            
            if response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Error in chat_without_image: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def get_suggested_questions(self, image_bytes: bytes) -> List[str]:
        """
        Generate suggested questions about an uploaded image.
        
        Args:
            image_bytes: The image data as bytes
            
        Returns:
            List of suggested questions
        """
        try:
            prompt = (
                "Look at this image and suggest 4 specific, detailed questions that someone might ask about it. "
                "Focus on location identification, product analysis, text reading, and contextual details. "
                "Make the questions specific to what you can actually see in the image. "
                "Return only the questions, one per line, without numbering."
            )
            
            # Convert image bytes to PIL Image
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            response = self.model.generate_content(
                [prompt, image],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=300,
                    temperature=0.8
                )
            )
            
            if response.text:
                questions = [q.strip() for q in response.text.split('\n') if q.strip()]
                return questions[:4]  # Return max 4 questions
            else:
                return [
                    "What do you see in this image?",
                    "Can you identify the specific location?",
                    "What products or brands can you identify?",
                    "Can you read any text or signs in the image?"
                ]
                
        except Exception as e:
            logger.error(f"Error generating suggested questions: {str(e)}")
            return [
                "What do you see in this image?",
                "Can you identify the specific location?",
                "What products or brands can you identify?",
                "Can you read any text or signs in the image?"
            ]
    
    def analyze_location_context(self, image_bytes: bytes, user_question: str) -> str:
        """
        Specialized analysis for location-related questions.
        
        Args:
            image_bytes: The image data as bytes
            user_question: User's location-related question
            
        Returns:
            AI response focused on location analysis
        """
        try:
            # Convert image bytes to PIL Image
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            location_prompt = f"""You are an expert location analyst. The user is asking: "{user_question}"

Please analyze this image with extreme attention to location details:

1. **Identify the Setting**: Indoor/outdoor, specific venue type
2. **Geographic Clues**: Architecture, signage, cultural indicators
3. **Specific Identifiers**: Street names, building names, landmarks
4. **Environmental Context**: Weather, lighting, time indicators
5. **Background Analysis**: What's visible that provides location context
6. **Text Recognition**: Any readable signs, addresses, or location markers

If you can identify the specific location, please provide:
- Exact location name if recognizable
- City, region, or country if determinable
- Confidence level in your identification
- Reasoning behind your conclusion

Be as detailed and specific as possible in your location analysis."""

            response = self.model.generate_content(
                [location_prompt, image],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1200,
                    temperature=0.3  # Lower temperature for more factual responses
                )
            )
            
            return response.text if response.text else "I couldn't analyze the location in this image."
            
        except Exception as e:
            logger.error(f"Error in location analysis: {str(e)}")
            return f"Sorry, I encountered an error analyzing the location: {str(e)}"
    
    def analyze_product_context(self, image_bytes: bytes, user_question: str) -> str:
        """
        Specialized analysis for product/e-commerce related questions.
        
        Args:
            image_bytes: The image data as bytes
            user_question: User's product-related question
            
        Returns:
            AI response focused on product analysis
        """
        try:
            # Convert image bytes to PIL Image
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            
            product_prompt = f"""You are an expert product analyst and e-commerce specialist. The user is asking: "{user_question}"

Please analyze this image with focus on products and commercial items:

1. **Product Identification**: What specific products/items do you see?
2. **Brand Recognition**: Identify any brands, logos, or trademarks
3. **Product Details**: 
   - Model numbers, product codes, specifications
   - Size, color, material descriptions
   - Condition and packaging status
4. **Text Analysis**: Read all visible text on products, labels, tags
5. **Price Information**: Any visible pricing or value indicators
6. **Market Analysis**: 
   - Product category and market segment
   - Quality assessment and authenticity indicators
   - Estimated value range or market positioning
7. **Comparative Analysis**: Similar products or alternatives
8. **Usage Context**: How/where the product is being used or displayed

If this is an e-commerce or retail context:
- Analyze the product presentation and marketing
- Identify any unique selling points or features
- Assess the product's appeal and target market

Be extremely detailed in your product analysis and provide specific identifications where possible."""

            response = self.model.generate_content(
                [product_prompt, image],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1200,
                    temperature=0.3  # Lower temperature for more factual responses
                )
            )
            
            return response.text if response.text else "I couldn't analyze the products in this image."
            
        except Exception as e:
            logger.error(f"Error in product analysis: {str(e)}")
            return f"Sorry, I encountered an error analyzing the products: {str(e)}"