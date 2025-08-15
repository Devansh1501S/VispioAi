"""
Services package initialization and factory methods.
"""

# Try to import the main services, fall back to fallback services if needed
try:
    from .gemini_service import GeminiService
    GEMINI_AVAILABLE = True
except ImportError:
    from .gemini_fallback import GeminiFallbackService as GeminiService
    GEMINI_AVAILABLE = False

try:
    from .audio_service import AudioService
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

try:
    from .chatbot_service import ChatbotService
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False

__all__ = ['GeminiService', 'AudioService', 'ChatbotService', 'ServiceFactory', 'GEMINI_AVAILABLE', 'AUDIO_AVAILABLE', 'CHATBOT_AVAILABLE']

class ServiceFactory:
    """Factory class for creating and managing services."""
    
    _instances = {}
    
    @classmethod
    def get_gemini_service(cls) -> GeminiService:
        """Get or create GeminiService instance."""
        if 'gemini' not in cls._instances:
            if GEMINI_AVAILABLE:
                cls._instances['gemini'] = GeminiService()
            else:
                # Use fallback service with API key from environment
                import os
                api_key = os.environ.get("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY not found in environment")
                cls._instances['gemini'] = GeminiService(api_key)
        return cls._instances['gemini']
    
    @classmethod
    def get_audio_service(cls) -> AudioService:
        """Get or create AudioService instance."""
        if not AUDIO_AVAILABLE:
            raise ImportError("AudioService not available")
        if 'audio' not in cls._instances:
            cls._instances['audio'] = AudioService()
        return cls._instances['audio']
    
    @classmethod
    def get_chatbot_service(cls) -> ChatbotService:
        """Get or create ChatbotService instance."""
        if not CHATBOT_AVAILABLE:
            raise ImportError("ChatbotService not available")
        if 'chatbot' not in cls._instances:
            cls._instances['chatbot'] = ChatbotService()
        return cls._instances['chatbot']
    
    @classmethod
    def clear_instances(cls):
        """Clear all cached service instances."""
        cls._instances.clear()
    
    @classmethod
    def verify_services(cls) -> bool:
        """Verify all services have required methods."""
        try:
            gemini = cls.get_gemini_service()
            
            # Check GeminiService methods
            required_gemini_methods = [
                'generate_caption', 'identify_location', 'identify_product',
                'comprehensive_analysis', 'extract_text_and_details'
            ]
            
            for method in required_gemini_methods:
                if not hasattr(gemini, method):
                    raise AttributeError(f"GeminiService missing method: {method}")
            
            # Only check other services if they're available
            if CHATBOT_AVAILABLE:
                chatbot = cls.get_chatbot_service()
                required_chatbot_methods = [
                    'chat_with_image', 'analyze_location_context', 'analyze_product_context'
                ]
                
                for method in required_chatbot_methods:
                    if not hasattr(chatbot, method):
                        raise AttributeError(f"ChatbotService missing method: {method}")
            
            return True
            
        except Exception as e:
            print(f"Service verification failed: {e}")
            return False