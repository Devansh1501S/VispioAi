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
    page_icon="logo.svg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
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
    padding: 1rem 0 0.5rem 0;
    background: linear-gradient(90deg, #FF6B35, #2E4BC6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.3rem;
    margin-bottom: 2rem;
    font-weight: 300;
}

.logo-container svg {
    width: 80px;
    height: 40px;
    margin-top: 1rem;
}

/* Hide Streamlit menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hide the hamburger menu */
.css-1rs6os {display: none;}
.css-17ziqus {display: none;}

/* Toggle switch styling */
.toggle-switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
    margin-top: 1.5rem;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 34px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: #2196F3;
}

input:checked + .slider:before {
    transform: translateX(26px);
}

/* Enhanced front page styling */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
    color: white;
}

.feature-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #FF6B35;
    transition: transform 0.2s;
}

.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* Settings button styling */
.stButton > button {
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.2s ease;
    border: 2px solid transparent;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Primary button for opening settings */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #FF6B35, #2E4BC6);
    border-color: #FF6B35;
}

/* Secondary button for closing settings */
.stButton > button[kind="secondary"] {
    background: linear-gradient(90deg, #dc3545, #6c757d);
    border-color: #dc3545;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header {
        font-size: 2.5rem;
    }
    .logo-container svg {
        width: 60px;
        height: 30px;
    }
    .toggle-switch {
        width: 50px;
        height: 28px;
    }
    .feature-card {
        margin: 0.5rem 0;
        padding: 1rem;
    }
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
    # Header with logo
    col_logo, col_title, col_theme = st.columns([1, 3, 1])
    
    with col_logo:
        with open("logo.svg", "r") as f:
            logo_svg = f.read()
        st.markdown(f'<div class="logo-container" style="text-align: center; padding-top: 1rem;">{logo_svg}</div>', unsafe_allow_html=True)
    
    with col_title:
        st.markdown('<div class="main-header">Vispio</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Let AI Speak Your Pictures</div>', unsafe_allow_html=True)
    
    with col_theme:
        # Theme toggle switch using Streamlit
        st.markdown("<br>", unsafe_allow_html=True)
        dark_mode = st.toggle("🌙 Dark Mode", key="theme_toggle")
        
        # Apply dark theme if enabled
        if dark_mode:
            st.markdown("""
            <style>
            .stApp {
                background-color: #0E1117 !important;
                color: #FAFAFA !important;
            }
            .feature-card {
                background: #262730 !important;
                color: #FAFAFA !important;
            }
            .hero-section {
                background: linear-gradient(135deg, #1f2937 0%, #374151 100%) !important;
            }
            </style>
            """, unsafe_allow_html=True)
    
    # Initialize services
    try:
        gemini_service, audio_service = initialize_services()
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        st.stop()
    
    # Settings toggle button in top area
    col_settings_btn, col_spacer = st.columns([1, 4])
    with col_settings_btn:
        # Toggle button for settings
        if st.button("⚙️ Settings" if not st.session_state.get('settings_open', False) else "✕ Close", 
                     type="primary" if not st.session_state.get('settings_open', False) else "secondary",
                     use_container_width=True):
            st.session_state.settings_open = not st.session_state.get('settings_open', False)
            st.rerun()
    
    # Conditional sidebar based on toggle state
    if st.session_state.get('settings_open', False):
        with st.sidebar:
            st.header("⚙️ Settings Panel")
            st.markdown("---")
            
            # Caption style selection
            caption_style = st.selectbox(
                "Caption Style",
                ["Descriptive", "Creative", "Technical", "Simple"],
                help="Choose the style of image caption you prefer"
            )
            
            st.markdown("---")
            
            # Advanced options
            with st.expander("🔧 Advanced Options"):
                max_tokens = st.slider("Max Caption Length", 50, 300, 150)
                temperature = st.slider("Creativity", 0.1, 1.0, 0.7, 0.1)
                
            st.markdown("---")
            
            # Close button at bottom of sidebar
            if st.button("✕ Close Settings", type="secondary", use_container_width=True):
                st.session_state.settings_open = False
                st.rerun()
                
            # Info section
            st.markdown("**💡 Quick Tips:**")
            st.markdown("- **Descriptive**: Detailed analysis")
            st.markdown("- **Creative**: Artistic storytelling")
            st.markdown("- **Technical**: Photography focus")
            st.markdown("- **Simple**: Brief description")
    else:
        # Default values when settings are closed
        caption_style = "Descriptive"
        max_tokens = 150
        temperature = 0.7
    
    # Set default audio settings
    audio_speed = 1.0
    audio_language = "en"
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h2 style="margin-bottom: 1rem;">Transform Your Images Into Stories</h2>
        <p style="font-size: 1.1rem; margin-bottom: 0;">Upload any image and watch as AI creates detailed captions and brings them to life with natural speech narration.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Smart Analysis</h4>
            <p>Advanced AI understands context, objects, and emotions in your images</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎨 Multiple Styles</h4>
            <p>Choose from descriptive, creative, technical, or simple caption styles</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f3:
        st.markdown("""
        <div class="feature-card">
            <h4>🔊 Audio Magic</h4>
            <p>Convert captions to natural speech with high-quality text-to-speech</p>
        </div>
        """, unsafe_allow_html=True)

    # Main content area with better spacing
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1], gap="large")
    
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
                
                # Audio generation section - centered button
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🎵 Generate Audio Narration", type="secondary", use_container_width=True):
                        with st.spinner("Generating audio narration..."):
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
    
    # Footer with About Us button
    st.markdown("---")
    
    # Center the about us button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🌟 About Us", type="secondary", use_container_width=True):
            st.session_state.show_about = True
            st.rerun()
    
    # About Us modal using expander
    if st.session_state.get('show_about', False):
        with st.expander("🌟 About Us", expanded=True):
            st.markdown("""
            <div style="padding: 1rem;">
                <h3 style="color: #2E4BC6; margin-bottom: 1rem;">Bringing Vision to Words with AI</h3>
                <p>At Vispio, we believe every image tells a story — and with the power of AI, we help you hear it.</p>
                
                <p>Vispio isn't just a tool — it's your smart visual companion that can see, understand, and speak about the world around you. Whether it's a photo, a document, or a moment captured on your phone, our AI transforms images into meaningful descriptions — in both text and audio.</p>
                
                <p>We're on a mission to make visual understanding seamless, accessible, and intelligent — for everyone.</p>
                
                <h4 style="color: #FF6B35; margin-top: 2rem; margin-bottom: 1rem;">🔍 What We Offer</h4>
                
                <div style="margin-left: 1rem;">
                    <h5 style="color: #2E4BC6;">Image to Text Conversion</h5>
                    <p>Upload any image and instantly receive an accurate, natural-language description generated by AI.</p>
                    
                    <h5 style="color: #2E4BC6;">Image to Audio Narration</h5>
                    <p>Let your images speak. Our AI reads the description aloud using clear, human-like voice synthesis.</p>
                    
                    <h5 style="color: #2E4BC6;">Downloadable Transcripts & Audio Files</h5>
                    <p>Save what matters. You can download both the text and the audio files for future use or sharing.</p>
                    
                    <h5 style="color: #2E4BC6;">Fast, Secure, and Simple</h5>
                    <p>A smooth experience designed for privacy and speed — your data stays yours.</p>
                </div>
                
                <h4 style="color: #FF6B35; margin-top: 2rem; margin-bottom: 1rem;">💡 Our Vision</h4>
                <p>To empower people with AI that sees and speaks, helping the world understand visuals through smart, voice-ready technology.</p>
                
                <h4 style="color: #FF6B35; margin-top: 2rem; margin-bottom: 1rem;">👥 Who We Are</h4>
                <p>We're passionate creators merging computer vision and AI to build tools that feel simple, powerful, and human-friendly.</p>
                
                <p style="text-align: center; margin-top: 2rem; color: #666; font-weight: bold;">Built with ❤️ by Devansh</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Close button functionality
            if st.button("✕ Close About", type="secondary", use_container_width=True):
                st.session_state.show_about = False
                st.rerun()

if __name__ == "__main__":
    # Initialize session state
    if 'image_uploaded' not in st.session_state:
        st.session_state.image_uploaded = False
    if 'caption_generated' not in st.session_state:
        st.session_state.caption_generated = False
    if 'audio_generated' not in st.session_state:
        st.session_state.audio_generated = False
    if 'settings_open' not in st.session_state:
        st.session_state.settings_open = False
    if 'show_about' not in st.session_state:
        st.session_state.show_about = False
    
    main()
