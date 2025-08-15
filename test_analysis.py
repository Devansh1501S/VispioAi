#!/usr/bin/env python3
"""
Test script for advanced image analysis features
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_analysis_features():
    """Test the advanced analysis features."""
    try:
        from services.gemini_service import GeminiService
        from services.chatbot_service import ChatbotService
        from PIL import Image
        import io
        
        print("🔍 Testing Advanced Analysis Features...")
        
        # Initialize services
        gemini_service = GeminiService()
        chatbot_service = ChatbotService()
        print("✅ Services initialized")
        
        # Create a simple test image (you can replace this with an actual image)
        # For testing, we'll create a simple colored rectangle
        test_image = Image.new('RGB', (400, 300), color='blue')
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        print("🖼️ Test image created")
        
        # Test location analysis
        print("\n📍 Testing Location Analysis...")
        try:
            location_result = gemini_service.identify_location(img_bytes)
            if location_result["success"]:
                print("✅ Location analysis successful")
                print(f"Preview: {location_result['location_analysis'][:100]}...")
            else:
                print("❌ Location analysis failed")
        except Exception as e:
            print(f"❌ Location analysis error: {e}")
        
        # Test product analysis
        print("\n🛍️ Testing Product Analysis...")
        try:
            product_result = gemini_service.identify_product(img_bytes)
            if product_result["success"]:
                print("✅ Product analysis successful")
                print(f"Preview: {product_result['product_analysis'][:100]}...")
            else:
                print("❌ Product analysis failed")
        except Exception as e:
            print(f"❌ Product analysis error: {e}")
        
        # Test comprehensive analysis
        print("\n🔬 Testing Comprehensive Analysis...")
        try:
            comprehensive_result = gemini_service.comprehensive_analysis(img_bytes)
            if comprehensive_result["success"]:
                print("✅ Comprehensive analysis successful")
                print(f"Preview: {comprehensive_result['comprehensive_analysis'][:100]}...")
            else:
                print("❌ Comprehensive analysis failed")
        except Exception as e:
            print(f"❌ Comprehensive analysis error: {e}")
        
        # Test text extraction
        print("\n📝 Testing Text Extraction...")
        try:
            text_result = gemini_service.extract_text_and_details(img_bytes)
            if text_result["success"]:
                print("✅ Text extraction successful")
                print(f"Preview: {text_result['text_analysis'][:100]}...")
            else:
                print("❌ Text extraction failed")
        except Exception as e:
            print(f"❌ Text extraction error: {e}")
        
        # Test chatbot specialized analysis
        print("\n💬 Testing Chatbot Specialized Analysis...")
        try:
            location_response = chatbot_service.analyze_location_context(img_bytes, "Where is this place?")
            print("✅ Chatbot location analysis successful")
            print(f"Preview: {location_response[:100]}...")
        except Exception as e:
            print(f"❌ Chatbot location analysis error: {e}")
        
        try:
            product_response = chatbot_service.analyze_product_context(img_bytes, "What product is this?")
            print("✅ Chatbot product analysis successful")
            print(f"Preview: {product_response[:100]}...")
        except Exception as e:
            print(f"❌ Chatbot product analysis error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis features test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_analysis_features()
    if success:
        print("\n🎉 Advanced analysis features test completed!")
        print("\n📋 Available Analysis Types:")
        print("1. 📍 Location Analysis - Identifies places, landmarks, and geographic context")
        print("2. 🛍️ Product Analysis - Identifies products, brands, and e-commerce details")
        print("3. 🔬 Comprehensive Analysis - Complete detailed analysis of everything")
        print("4. 📝 Text Extraction - Extracts and analyzes all visible text")
        print("5. 💬 Smart Chatbot - Automatically routes questions to specialized analysis")
    else:
        print("\n❌ Analysis features test failed!")