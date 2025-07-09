import os
import tempfile
import logging
from typing import Optional
import gtts
import pygame
import io
from pydub import AudioSegment
from pydub.playback import play

class AudioService:
    """Service for handling text-to-speech conversion and audio processing."""
    
    def __init__(self):
        """Initialize the audio service."""
        self.temp_dir = tempfile.mkdtemp()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
        except Exception as e:
            self.logger.warning(f"Could not initialize pygame mixer: {e}")
    
    def text_to_speech(
        self, 
        text: str, 
        language: str = "en", 
        speed: float = 1.0,
        output_format: str = "wav"
    ) -> str:
        """
        Convert text to speech using gTTS.
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'es', 'fr')
            speed: Speech speed multiplier (0.5 to 2.0)
            output_format: Output audio format ('wav', 'mp3')
            
        Returns:
            Path to the generated audio file
            
        Raises:
            Exception: If TTS conversion fails
        """
        try:
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")
            
            self.logger.info(f"Converting text to speech: {text[:50]}...")
            
            # Create gTTS object
            tts = gtts.gTTS(
                text=text,
                lang=language,
                slow=False  # We'll handle speed adjustment separately
            )
            
            # Save to temporary MP3 file first
            temp_mp3_path = os.path.join(self.temp_dir, f"temp_audio_{id(text)}.mp3")
            tts.save(temp_mp3_path)
            
            # Load with pydub for speed adjustment and format conversion
            audio = AudioSegment.from_mp3(temp_mp3_path)
            
            # Adjust speed if needed
            if speed != 1.0:
                # Change speed without changing pitch
                audio = audio.speedup(playback_speed=speed)
            
            # Convert to requested format
            output_path = os.path.join(self.temp_dir, f"audio_{id(text)}.{output_format}")
            
            if output_format.lower() == "wav":
                audio.export(output_path, format="wav")
            elif output_format.lower() == "mp3":
                audio.export(output_path, format="mp3")
            else:
                raise ValueError(f"Unsupported audio format: {output_format}")
            
            # Clean up temporary MP3 file
            try:
                os.remove(temp_mp3_path)
            except:
                pass
            
            self.logger.info(f"Audio generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error in text-to-speech conversion: {str(e)}")
            raise Exception(f"Failed to convert text to speech: {str(e)}")
    
    def get_audio_duration(self, audio_path: str) -> float:
        """
        Get the duration of an audio file in seconds.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Duration in seconds
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # Convert milliseconds to seconds
        except Exception as e:
            self.logger.error(f"Error getting audio duration: {str(e)}")
            return 0.0
    
    def adjust_audio_speed(self, audio_path: str, speed: float) -> str:
        """
        Adjust the speed of an existing audio file.
        
        Args:
            audio_path: Path to the input audio file
            speed: Speed multiplier (0.5 to 2.0)
            
        Returns:
            Path to the speed-adjusted audio file
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            adjusted_audio = audio.speedup(playback_speed=speed)
            
            # Create new file path
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            output_path = os.path.join(self.temp_dir, f"{base_name}_speed_{speed}.wav")
            
            adjusted_audio.export(output_path, format="wav")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error adjusting audio speed: {str(e)}")
            raise Exception(f"Failed to adjust audio speed: {str(e)}")
    
    def convert_audio_format(self, input_path: str, output_format: str) -> str:
        """
        Convert audio file to different format.
        
        Args:
            input_path: Path to input audio file
            output_format: Target format ('wav', 'mp3', 'ogg')
            
        Returns:
            Path to converted audio file
        """
        try:
            audio = AudioSegment.from_file(input_path)
            
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(self.temp_dir, f"{base_name}.{output_format}")
            
            audio.export(output_path, format=output_format)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error converting audio format: {str(e)}")
            raise Exception(f"Failed to convert audio format: {str(e)}")
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files."""
        try:
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            self.logger.info("Temporary audio files cleaned up")
        except Exception as e:
            self.logger.error(f"Error cleaning up temporary files: {str(e)}")
    
    def get_supported_languages(self) -> dict:
        """
        Get list of supported languages for TTS.
        
        Returns:
            Dictionary mapping language codes to language names
        """
        return {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "ar": "Arabic",
            "hi": "Hindi"
        }
    
    def validate_language(self, language_code: str) -> bool:
        """
        Validate if a language code is supported.
        
        Args:
            language_code: Language code to validate
            
        Returns:
            True if supported, False otherwise
        """
        supported_languages = self.get_supported_languages()
        return language_code in supported_languages
