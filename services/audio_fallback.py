"""
Fallback Audio service using gtts
This is used when the main audio service fails to import
"""

import os
import tempfile
from gtts import gTTS

class AudioFallbackService:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def text_to_speech(self, text, speed=1.0, language="en"):
        """Convert text to speech using gTTS."""
        try:
            # Create a temporary file for the audio
            timestamp = int(os.path.getmtime(tempfile.mktemp()))
            audio_filename = f"audio_{timestamp}.mp3"
            audio_path = os.path.join(self.temp_dir, audio_filename)
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save the audio file
            tts.save(audio_path)
            
            return audio_path
            
        except Exception as e:
            raise Exception(f"Error generating audio: {str(e)}")
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files."""
        try:
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")
