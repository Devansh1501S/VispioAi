"""
Fallback Chatbot service using HTTP requests to Gemini API
This is used when the main chatbot service fails to import
"""

import requests
import json
import base64
from PIL import Image
import io

class ChatbotFallbackService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-1.5-flash"
    
    def chat_with_image(self, image_bytes, question, chat_history=None):
        """Chat with image using direct HTTP request."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Build context from chat history
            context = ""
            if chat_history:
                context = "Previous conversation:\n"
                for msg in chat_history[-5:]:  # Last 5 messages for context
                    if msg["role"] == "user":
                        context += f"User: {msg['content']}\n"
                    else:
                        context += f"AI: {msg['content']}\n"
                context += "\n"
            
            prompt = f"{context}Based on this image, please answer: {question}"
            
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": img_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 500,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text']
            
            return "I'm sorry, I couldn't process your question about the image."
            
        except Exception as e:
            return f"Error processing image chat: {str(e)}"
    
    def chat_without_image(self, question, chat_history=None):
        """Chat without image using direct HTTP request."""
        try:
            # Build context from chat history
            context = ""
            if chat_history:
                context = "Previous conversation:\n"
                for msg in chat_history[-5:]:  # Last 5 messages for context
                    if msg["role"] == "user":
                        context += f"User: {msg['content']}\n"
                    else:
                        context += f"AI: {msg['content']}\n"
                context += "\n"
            
            prompt = f"{context}Please answer: {question}"
            
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 500,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text']
            
            return "I'm sorry, I couldn't process your question."
            
        except Exception as e:
            return f"Error processing chat: {str(e)}"
    
    def analyze_location_context(self, image_bytes, question):
        """Analyze location context in image."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = f"""Analyze this image for location information and answer: {question}
            
            Focus on:
            - Geographic features
            - Landmarks or buildings
            - Street signs or location indicators
            - Cultural or architectural clues
            - Any text that might indicate location"""
            
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": img_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 400,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text']
            
            return "I couldn't analyze the location context in this image."
            
        except Exception as e:
            return f"Error analyzing location: {str(e)}"
    
    def analyze_product_context(self, image_bytes, question):
        """Analyze product context in image."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = f"""Analyze this image for product information and answer: {question}
            
            Focus on:
            - Product names and brands
            - Product features and specifications
            - Price information if visible
            - Product categories
            - Any text or labels on products"""
            
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": img_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "maxOutputTokens": 400,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text']
            
            return "I couldn't analyze the product context in this image."
            
        except Exception as e:
            return f"Error analyzing product: {str(e)}"
    
    def get_suggested_questions(self, image_bytes):
        """Get suggested questions for an image."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = """Based on this image, suggest 3-5 interesting questions that someone might ask about it.
            Make the questions diverse and engaging, covering different aspects like:
            - What objects or people are visible
            - Where this might be located
            - What's happening in the scene
            - Technical or artistic aspects
            
            Return only the questions, one per line, without numbering."""
            
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": img_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 300,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    questions_text = content['parts'][0]['text']
                    # Split by lines and clean up
                    questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
                    return questions[:5]  # Return max 5 questions
            
            return [
                "What do you see in this image?",
                "Can you describe the main elements?",
                "What's happening in this scene?"
            ]
            
        except Exception as e:
            return [
                "What do you see in this image?",
                "Can you describe the main elements?",
                "What's happening in this scene?"
            ]
