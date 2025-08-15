"""
Fallback Gemini service using direct HTTP requests
This is used when the google-generativeai library fails to install
"""

import requests
import json
import base64
from PIL import Image
import io

class GeminiFallbackService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-1.5-flash"
    
    def generate_caption(self, image_bytes, style="descriptive", max_tokens=150, temperature=0.7):
        """Generate caption using direct HTTP request to Gemini API."""
        try:
            # Convert bytes to base64
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Create style-specific prompts
            style_prompts = {
                "descriptive": "Provide a detailed, descriptive caption for this image. Focus on what you see, colors, composition, and context.",
                "creative": "Create a creative, artistic caption for this image. Use imaginative language and storytelling elements.",
                "technical": "Provide a technical analysis of this image. Focus on photography aspects, composition, lighting, and technical details.",
                "simple": "Give a simple, straightforward description of what you see in this image."
            }
            
            prompt = style_prompts.get(style.lower(), style_prompts["descriptive"])
            
            # Prepare the request
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            },
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
                    "temperature": temperature,
                    "topK": 32,
                    "topP": 1,
                    "maxOutputTokens": max_tokens,
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the text from the response
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text']
            
            return "Sorry, I couldn't generate a caption at this time."
            
        except Exception as e:
            return f"Error generating caption: {str(e)}"
    
    def identify_location(self, image_bytes):
        """Identify location in image using direct HTTP request."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = """Analyze this image and identify the location, landmarks, or geographical features. 
            Provide detailed information about where this might be, including:
            - Country/region
            - City or specific location
            - Notable landmarks or buildings
            - Any geographical features visible
            - Cultural or architectural indicators"""
            
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
                    location_analysis = content['parts'][0]['text']
                    return {"location_analysis": location_analysis}
            
            return {"location_analysis": "Location analysis failed"}
            
        except Exception as e:
            return {"location_analysis": f"Error analyzing location: {str(e)}"}
    
    def identify_product(self, image_bytes):
        """Identify product in image using direct HTTP request."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = """Analyze this image and identify any products, brands, or commercial items visible. 
            Provide detailed information about:
            - Product names and types
            - Brand names if visible
            - Product features and specifications
            - Any text or labels on the products
            - Estimated value or category"""
            
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
                    product_analysis = content['parts'][0]['text']
                    return {"product_analysis": product_analysis}
            
            return {"product_analysis": "Product analysis failed"}
            
        except Exception as e:
            return {"product_analysis": f"Error analyzing product: {str(e)}"}
    
    def comprehensive_analysis(self, image_bytes):
        """Comprehensive image analysis using direct HTTP request."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = """Provide a comprehensive analysis of this image covering:
            1. Visual elements (objects, people, animals, etc.)
            2. Colors, lighting, and composition
            3. Setting and context
            4. Mood and atmosphere
            5. Any text or symbols visible
            6. Potential location or time period
            7. Cultural or historical significance
            8. Technical aspects (photography, art style, etc.)"""
            
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
                    "temperature": 0.4,
                    "maxOutputTokens": 800,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    comprehensive_analysis = content['parts'][0]['text']
                    return {"comprehensive_analysis": comprehensive_analysis}
            
            return {"comprehensive_analysis": "Comprehensive analysis failed"}
            
        except Exception as e:
            return {"comprehensive_analysis": f"Error in comprehensive analysis: {str(e)}"}
    
    def extract_text_and_details(self, image_bytes):
        """Extract text and details from image using direct HTTP request."""
        try:
            img_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = """Extract and analyze all text visible in this image. Provide:
            1. All readable text content
            2. Text location and context
            3. Font styles or formatting if notable
            4. Language identification
            5. Meaning or purpose of the text
            6. Any numbers, dates, or important information
            7. Text quality and readability assessment"""
            
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
                    "temperature": 0.2,
                    "maxOutputTokens": 600,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    text_analysis = content['parts'][0]['text']
                    return {"text_analysis": text_analysis}
            
            return {"text_analysis": "Text extraction failed"}
            
        except Exception as e:
            return {"text_analysis": f"Error extracting text: {str(e)}"}
    
    def analyze_image(self, image, prompt="Describe this image in detail"):
        """Legacy method for backward compatibility."""
        try:
            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            # Use the new method
            return self.generate_caption(img_bytes, style="descriptive")
            
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def generate_text(self, prompt):
        """Generate text using direct HTTP request to Gemini API."""
        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the text from the response
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    return content['parts'][0]['text']
            
            return "Sorry, I couldn't generate a response at this time."
            
        except Exception as e:
            return f"Error generating text: {str(e)}"
