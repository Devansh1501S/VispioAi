"""
Services package initialization and factory methods.
"""

from .gemini_service import GeminiService
from .audio_service import AudioService
from .chatbot_service import ChatbotService

__all__ = ['GeminiService', 'AudioService', 'ChatbotService', 'ServiceFactory']

class ServiceFactory:
    """Factory class for creating and managing services."""
    
    _instances = {}
    
    @classmethod
    def get_gemini_service(cls) -> GeminiService:
        """Get or create GeminiService instance."""
        if 'gemini' not in cls._instances:
            cls._instances['gemini'] = GeminiService()
        return cls._instances['gemini']
    
    @classmethod
    def get_audio_service(cls) -> AudioService:
        """Get or create AudioService instance."""
        if 'audio' not in cls._instances:
            cls._instances['audio'] = AudioService()
        return cls._instances['audio']
    
    @classmethod
    def get_chatbot_service(cls) -> ChatbotService:
        """Get or create ChatbotService instance."""
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
            chatbot = cls.get_chatbot_service()
            audio = cls.get_audio_service()
            
            # Check GeminiService methods
            required_gemini_methods = [
                'generate_caption', 'identify_location', 'identify_product',
                'comprehensive_analysis', 'extract_text_and_details'
            ]
            
            for method in required_gemini_methods:
                if not hasattr(gemini, method):
                    raise AttributeError(f"GeminiService missing method: {method}")
            
            # Check ChatbotService methods
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