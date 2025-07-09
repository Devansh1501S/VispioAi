import streamlit as st
import io
import os
import base64
from PIL import Image
import time
from services.gemini_service import GeminiService
from services.audio_service import AudioService
from utils.image_utils import validate_image, resize_image

# Page configuration
st.set_page_config(
    page_title="Vispio - AI Image Captioning",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def initialize_services():
    gemini_service = GeminiService()
    audio_service = AudioService()
    return gemini_service, audio_service

# Custom CSS for enhanced styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem 0;
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 2rem;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.upload-section {
    border: 2px dashed #FF6B6B;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}

.caption-box {
    background-color: #F8F9FA;
    border-left: 4px solid #FF6B6B;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}

.audio-controls {
    background-color: #F0F2F6;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.download-section {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 1rem 0;
}

.error-message {
    background-color: #FFE6E6;
    border: 1px solid #FF6B6B;
    color: #D63031;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}

.success-message {
    background-color: #E6F7FF;
    border: 1px solid #4ECDC4;
    color: #00B894;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">👁️ Vispio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-Powered Image Captioning with Audio Narration</div>', unsafe_allow_html=True)
    
    # Initialize services
    try:
        gemini_service, audio_service = initialize_services()
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        st.stop()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Caption style selection
        caption_style = st.selectbox(
            "Caption Style",
            ["Descriptive", "Creative", "Technical", "Simple"],
            help="Choose the style of image caption you prefer"
        )
        
        # Audio settings
        st.subheader("🔊 Audio Settings")
        audio_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
        audio_language = st.selectbox("Language", ["en", "es", "fr", "de", "it"])
        
        # Advanced options
        with st.expander("Advanced Options"):
            max_tokens = st.slider("Max Caption Length", 50, 300, 150)
            temperature = st.slider("Creativity", 0.1, 1.0, 0.7, 0.1)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📷 Image Upload")
        
        # File uploader with drag and drop
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
            help="Drag and drop an image or click to browse"
        )
        
        # Image preview
        if uploaded_file is not None:
            try:
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                
                # Validate and process image
                image = Image.open(uploaded_file)
                
                # Basic validation without calling verify() which can consume the image
                if image.size[0] < 10 or image.size[1] < 10:
                    st.error("Image is too small. Please upload a larger image.")
                    st.stop()
                
                if image.size[0] * image.size[1] > 100_000_000:
                    st.error("Image is too large. Please upload a smaller image.")
                    st.stop()
                
                # Resize image if too large
                display_image = resize_image(image, max_size=(800, 600))
                
                st.image(display_image, caption="Uploaded Image", use_container_width=True)
                
                # Store image in session state
                st.session_state.current_image = image
                st.session_state.image_uploaded = True
                
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.stop()
    
    with col2:
        st.subheader("📝 Generated Caption")
        
        if 'current_image' in st.session_state and st.session_state.image_uploaded:
            # Generate caption button
            if st.button("🚀 Generate Caption", type="primary", use_container_width=True):
                with st.spinner("Generating caption..."):
                    try:
                        # Optimize image for API
                        from utils.image_utils import optimize_image_for_api
                        img_bytes = optimize_image_for_api(st.session_state.current_image, max_file_size_mb=2.0)
                        
                        # Generate caption using Gemini
                        caption = gemini_service.generate_caption(
                            img_bytes, 
                            style=caption_style.lower(),
                            max_tokens=max_tokens,
                            temperature=temperature
                        )
                        
                        st.session_state.generated_caption = caption
                        st.session_state.caption_generated = True
                        
                        # Success message
                        st.markdown('<div class="success-message">✅ Caption generated successfully!</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.markdown(f'<div class="error-message">❌ Error generating caption: {str(e)}</div>', unsafe_allow_html=True)
            
            # Display and edit caption
            if 'generated_caption' in st.session_state and st.session_state.caption_generated:
                st.markdown('<div class="caption-box">', unsafe_allow_html=True)
                
                # Editable caption
                edited_caption = st.text_area(
                    "Edit Caption (optional)",
                    value=st.session_state.generated_caption,
                    height=100,
                    help="You can edit the caption before generating audio"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Audio generation section
                st.subheader("🔊 Audio Narration")
                
                col_audio1, col_audio2 = st.columns([1, 1])
                
                with col_audio1:
                    if st.button("🎵 Generate Audio", use_container_width=True):
                        with st.spinner("Generating audio..."):
                            try:
                                audio_file = audio_service.text_to_speech(
                                    edited_caption,
                                    speed=audio_speed,
                                    language=audio_language
                                )
                                
                                st.session_state.audio_file = audio_file
                                st.session_state.audio_generated = True
                                st.session_state.final_caption = edited_caption
                                
                                st.success("Audio generated successfully!")
                                
                            except Exception as e:
                                st.error(f"Error generating audio: {str(e)}")
                
                # Audio player and download options
                if 'audio_generated' in st.session_state and st.session_state.audio_generated:
                    st.markdown('<div class="audio-controls">', unsafe_allow_html=True)
                    
                    # Audio player
                    with open(st.session_state.audio_file, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/wav')
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download section
                    st.subheader("💾 Download Options")
                    
                    col_dl1, col_dl2 = st.columns([1, 1])
                    
                    with col_dl1:
                        # Download caption as text
                        st.download_button(
                            label="📄 Download Caption (TXT)",
                            data=st.session_state.final_caption,
                            file_name=f"vispio_caption_{int(time.time())}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col_dl2:
                        # Download audio
                        with open(st.session_state.audio_file, "rb") as audio_file:
                            st.download_button(
                                label="🎵 Download Audio (WAV)",
                                data=audio_file.read(),
                                file_name=f"vispio_audio_{int(time.time())}.wav",
                                mime="audio/wav",
                                use_container_width=True
                            )
        else:
            st.info("👆 Please upload an image to start generating captions.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🚀 Powered by <strong>Vispio</strong> | Google Gemini Vision API</p>
            <p>Made with ❤️ using Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    # Initialize session state
    if 'image_uploaded' not in st.session_state:
        st.session_state.image_uploaded = False
    if 'caption_generated' not in st.session_state:
        st.session_state.caption_generated = False
    if 'audio_generated' not in st.session_state:
        st.session_state.audio_generated = False
    
    main()
