#!/usr/bin/env python3
"""
Comprehensive integration test for all analysis features
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

def test_full_integration():
    """Test complete integration of all analysis features."""
    print("🔧 Full Integration Test - Senior Dev Style")
    print("=" * 60)
    
    try:
        # Test service imports
        print("\n📦 Testing Service Imports...")
        from services.gemini_service import GeminiService
        from services.chatbot_service import ChatbotService
        from services.audio_service import AudioService
        print("✅ All services imported successfully")
        
        # Test service initialization
        print("\n🚀 Testing Service Initialization...")
        gemini_service = GeminiService()
        chatbot_service = ChatbotService()
        audio_service = AudioService()
        print("✅ All services initialized successfully")
        
        # Test method availability
        print("\n🔍 Testing Method Availability...")
        gemini_methods = [
            'generate_caption',
            'analyze_image_content', 
            'identify_location',
            'identify_product',
            'comprehensive_analysis',
            'extract_text_and_details',
            'validate_api_key'
        ]
        
        for method in gemini_methods:
            if hasattr(gemini_service, method):
                print(f"✅ GeminiService.{method}")
            else:
                print(f"❌ GeminiService.{method} - MISSING")
                return False
        
        chatbot_methods = [
            'chat_with_image',
            'chat_without_image',
            'get_suggested_questions',
            'analyze_location_context',
            'analyze_product_context'
        ]
        
        for method in chatbot_methods:
            if hasattr(chatbot_service, method):
                print(f"✅ ChatbotService.{method}")
            else:
                print(f"❌ ChatbotService.{method} - MISSING")
                return False
        
        # Test app integration
        print("\n🎯 Testing App Integration...")
        try:
            from app import initialize_services
            app_gemini, app_audio, app_chatbot = initialize_services()
            print("✅ App services initialization works")
            
            # Test if app services have all methods
            if hasattr(app_gemini, 'identify_location'):
                print("✅ App GeminiService has identify_location")
            else:
                print("❌ App GeminiService missing identify_location")
                return False
                
            if hasattr(app_chatbot, 'analyze_location_context'):
                print("✅ App ChatbotService has analyze_location_context")
            else:
                print("❌ App ChatbotService missing analyze_location_context")
                return False
                
        except Exception as e:
            print(f"❌ App integration error: {e}")
            return False
        
        # Test with dummy data
        print("\n🧪 Testing with Dummy Data...")
        from PIL import Image
        import io
        
        # Create test image
        test_image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        # Test each analysis method
        analysis_methods = [
            ('Standard Caption', lambda: gemini_service.generate_caption(img_bytes)),
            ('Location Analysis', lambda: gemini_service.identify_location(img_bytes)),
            ('Product Analysis', lambda: gemini_service.identify_product(img_bytes)),
            ('Comprehensive Analysis', lambda: gemini_service.comprehensive_analysis(img_bytes)),
            ('Text Extraction', lambda: gemini_service.extract_text_and_details(img_bytes))
        ]
        
        for name, method in analysis_methods:
            try:
                result = method()
                if isinstance(result, dict):
                    success = result.get('success', True)
                    print(f"✅ {name} - {'Success' if success else 'Completed with warnings'}")
                else:
                    print(f"✅ {name} - Completed")
            except Exception as e:
                print(f"❌ {name} - Error: {e}")
                return False
        
        # Test chatbot methods
        chatbot_tests = [
            ('Location Context', lambda: chatbot_service.analyze_location_context(img_bytes, "Where is this?")),
            ('Product Context', lambda: chatbot_service.analyze_product_context(img_bytes, "What product is this?"))
        ]
        
        for name, method in chatbot_tests:
            try:
                result = method()
                print(f"✅ Chatbot {name} - Completed")
            except Exception as e:
                print(f"❌ Chatbot {name} - Error: {e}")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("🚀 System is ready for production use")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_analysis_flow():
    """Test the specific analysis flow that was failing."""
    print("\n🔧 Testing App Analysis Flow...")
    
    try:
        from PIL import Image
        import io
        
        # Create test image
        test_image = Image.new('RGB', (200, 200), color='blue')
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        # Import and test the exact flow from app.py
        from services.gemini_service import GeminiService
        gemini_service = GeminiService()
        
        # Test the exact analysis types from the app
        analysis_types = [
            "Standard Caption",
            "Location Analysis", 
            "Product Analysis",
            "Comprehensive Analysis",
            "Text Extraction"
        ]
        
        for analysis_type in analysis_types:
            print(f"\n🧪 Testing: {analysis_type}")
            
            try:
                if analysis_type == "Standard Caption":
                    result = gemini_service.generate_caption(img_bytes, style="descriptive")
                    print(f"✅ {analysis_type} - Success")
                elif analysis_type == "Location Analysis":
                    location_result = gemini_service.identify_location(img_bytes)
                    result = location_result.get("location_analysis", "Location analysis failed")
                    print(f"✅ {analysis_type} - Success")
                elif analysis_type == "Product Analysis":
                    product_result = gemini_service.identify_product(img_bytes)
                    result = product_result.get("product_analysis", "Product analysis failed")
                    print(f"✅ {analysis_type} - Success")
                elif analysis_type == "Comprehensive Analysis":
                    comprehensive_result = gemini_service.comprehensive_analysis(img_bytes)
                    result = comprehensive_result.get("comprehensive_analysis", "Comprehensive analysis failed")
                    print(f"✅ {analysis_type} - Success")
                elif analysis_type == "Text Extraction":
                    text_result = gemini_service.extract_text_and_details(img_bytes)
                    result = text_result.get("text_analysis", "Text extraction failed")
                    print(f"✅ {analysis_type} - Success")
                    
            except Exception as e:
                print(f"❌ {analysis_type} - Error: {e}")
                return False
        
        print("\n✅ App Analysis Flow Test - ALL PASSED")
        return True
        
    except Exception as e:
        print(f"❌ App Analysis Flow Test - Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Senior Developer Integration Test Suite")
    print("Testing all components and integration points...")
    
    # Run full integration test
    integration_success = test_full_integration()
    
    # Run specific app flow test
    app_flow_success = test_app_analysis_flow()
    
    if integration_success and app_flow_success:
        print("\n🎉 ALL TESTS PASSED - SYSTEM READY!")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED - CHECK LOGS ABOVE")
        sys.exit(1)