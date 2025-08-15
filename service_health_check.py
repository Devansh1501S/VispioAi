#!/usr/bin/env python3
"""
Service health check for production deployment
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

def comprehensive_health_check():
    """Comprehensive health check for all services and methods."""
    print("🏥 Service Health Check - Production Ready")
    print("=" * 60)
    
    health_status = {
        'environment': False,
        'imports': False,
        'initialization': False,
        'methods': False,
        'api_connectivity': False,
        'integration': False
    }
    
    # 1. Environment Check
    print("\n🔑 Environment Variables Check...")
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key and len(api_key) > 10:
            print("✅ GEMINI_API_KEY is set and valid length")
            health_status['environment'] = True
        else:
            print("❌ GEMINI_API_KEY is missing or invalid")
            return health_status
    except Exception as e:
        print(f"❌ Environment check failed: {e}")
        return health_status
    
    # 2. Import Check
    print("\n📦 Import Check...")
    try:
        from services import ServiceFactory, GeminiService, AudioService, ChatbotService
        print("✅ All service imports successful")
        health_status['imports'] = True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return health_status
    
    # 3. Service Initialization Check
    print("\n🚀 Service Initialization Check...")
    try:
        gemini_service = ServiceFactory.get_gemini_service()
        audio_service = ServiceFactory.get_audio_service()
        chatbot_service = ServiceFactory.get_chatbot_service()
        print("✅ All services initialized successfully")
        health_status['initialization'] = True
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return health_status
    
    # 4. Method Availability Check
    print("\n🔍 Method Availability Check...")
    try:
        # Check GeminiService methods
        gemini_methods = [
            'generate_caption', 'analyze_image_content', 'identify_location',
            'identify_product', 'comprehensive_analysis', 'extract_text_and_details'
        ]
        
        for method in gemini_methods:
            if hasattr(gemini_service, method):
                print(f"✅ GeminiService.{method}")
            else:
                print(f"❌ GeminiService.{method} - MISSING")
                return health_status
        
        # Check ChatbotService methods
        chatbot_methods = [
            'chat_with_image', 'chat_without_image', 'get_suggested_questions',
            'analyze_location_context', 'analyze_product_context'
        ]
        
        for method in chatbot_methods:
            if hasattr(chatbot_service, method):
                print(f"✅ ChatbotService.{method}")
            else:
                print(f"❌ ChatbotService.{method} - MISSING")
                return health_status
        
        # Check AudioService methods
        audio_methods = ['text_to_speech', 'get_audio_duration']
        
        for method in audio_methods:
            if hasattr(audio_service, method):
                print(f"✅ AudioService.{method}")
            else:
                print(f"❌ AudioService.{method} - MISSING")
                return health_status
        
        health_status['methods'] = True
        
    except Exception as e:
        print(f"❌ Method check failed: {e}")
        return health_status
    
    # 5. API Connectivity Check
    print("\n🌐 API Connectivity Check...")
    try:
        # Test API key validation
        if gemini_service.validate_api_key():
            print("✅ Gemini API connectivity successful")
            health_status['api_connectivity'] = True
        else:
            print("❌ Gemini API connectivity failed")
            return health_status
    except Exception as e:
        print(f"❌ API connectivity check failed: {e}")
        return health_status
    
    # 6. Integration Test
    print("\n🧪 Integration Test...")
    try:
        from PIL import Image
        import io
        
        # Create test image
        test_image = Image.new('RGB', (100, 100), color='green')
        img_byte_arr = io.BytesIO()
        test_image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        # Test each analysis type
        analysis_tests = [
            ('Caption', lambda: gemini_service.generate_caption(img_bytes)),
            ('Location', lambda: gemini_service.identify_location(img_bytes)),
            ('Product', lambda: gemini_service.identify_product(img_bytes)),
            ('Comprehensive', lambda: gemini_service.comprehensive_analysis(img_bytes)),
            ('Text', lambda: gemini_service.extract_text_and_details(img_bytes))
        ]
        
        for name, test_func in analysis_tests:
            try:
                result = test_func()
                print(f"✅ {name} Analysis - Working")
            except Exception as e:
                print(f"❌ {name} Analysis - Error: {e}")
                return health_status
        
        # Test chatbot functions
        chatbot_tests = [
            ('Location Context', lambda: chatbot_service.analyze_location_context(img_bytes, "Where is this?")),
            ('Product Context', lambda: chatbot_service.analyze_product_context(img_bytes, "What is this?"))
        ]
        
        for name, test_func in chatbot_tests:
            try:
                result = test_func()
                print(f"✅ Chatbot {name} - Working")
            except Exception as e:
                print(f"❌ Chatbot {name} - Error: {e}")
                return health_status
        
        health_status['integration'] = True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return health_status
    
    return health_status

def print_health_summary(health_status):
    """Print health check summary."""
    print("\n" + "=" * 60)
    print("📊 HEALTH CHECK SUMMARY")
    print("=" * 60)
    
    total_checks = len(health_status)
    passed_checks = sum(health_status.values())
    
    for check, status in health_status.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check.replace('_', ' ').title()}")
    
    print(f"\n📈 Overall Health: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 SYSTEM IS HEALTHY AND READY FOR PRODUCTION!")
        return True
    else:
        print("⚠️ SYSTEM HAS ISSUES - CHECK FAILED COMPONENTS")
        return False

if __name__ == "__main__":
    health_status = comprehensive_health_check()
    system_healthy = print_health_summary(health_status)
    
    sys.exit(0 if system_healthy else 1)