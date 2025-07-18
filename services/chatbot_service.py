"""
Chatbot service for interactive conversations about images using Gemini API.
"""

import os
import logging
from typing import List, Dict, Optional, Any
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class ChatbotService:
    """Service for handling chatbot conversations with Gemini API."""
    
    def __init__(self):
        """Initialize the chatbot service with Gemini API client."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        
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
            # Build conversation context
            contents = []
            
            # Add chat history if available
            if chat_history:
                for message in chat_history[-10:]:  # Keep last 10 messages for context
                    if message["role"] == "user":
                        contents.append(types.Content(
                            role="user", 
                            parts=[types.Part(text=message["content"])]
                        ))
                    elif message["role"] == "assistant":
                        contents.append(types.Content(
                            role="model", 
                            parts=[types.Part(text=message["content"])]
                        ))
            
            # Add current image and message
            parts = [
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                ),
                types.Part(text=user_message)
            ]
            
            contents.append(types.Content(role="user", parts=parts))
            
            # System instruction for better responses
            system_instruction = (
                "You are a helpful AI assistant that can see and understand images. "
                "Provide detailed, accurate, and conversational responses about what you see. "
                "Be friendly and engaging while maintaining accuracy. "
                "If asked about specific details in the image, focus on those areas. "
                "Keep responses informative but conversational."
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
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
            # Build conversation context
            contents = []
            
            # Add chat history if available
            if chat_history:
                for message in chat_history[-10:]:  # Keep last 10 messages for context
                    if message["role"] == "user":
                        contents.append(types.Content(
                            role="user", 
                            parts=[types.Part(text=message["content"])]
                        ))
                    elif message["role"] == "assistant":
                        contents.append(types.Content(
                            role="model", 
                            parts=[types.Part(text=message["content"])]
                        ))
            
            # Add current message
            contents.append(types.Content(
                role="user", 
                parts=[types.Part(text=user_message)]
            ))
            
            # System instruction for general chat
            system_instruction = (
                "You are Vispio's AI assistant, specialized in visual understanding and image analysis. "
                "While you can chat about general topics, your expertise is in helping users understand "
                "and describe visual content. Be helpful, friendly, and encourage users to upload images "
                "for visual analysis when relevant."
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
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
                "Look at this image and suggest 4 interesting questions that someone might ask about it. "
                "Focus on specific details, context, or analysis. "
                "Return only the questions, one per line, without numbering."
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg"
                    ),
                    types.Part(text=prompt)
                ],
                config=types.GenerateContentConfig(
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
                    "Can you describe the main subject?",
                    "What's the setting or location?",
                    "Are there any interesting details?"
                ]
                
        except Exception as e:
            logger.error(f"Error generating suggested questions: {str(e)}")
            return [
                "What do you see in this image?",
                "Can you describe the main subject?",
                "What's the setting or location?",
                "Are there any interesting details?"
            ]