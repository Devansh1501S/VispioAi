import streamlit as st
import os
import io
from PIL import Image
import time

# Cache busting for Streamlit Cloud deployment
def clear_all_caches():
    """Clear all Streamlit caches to prevent deployment issues."""
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
        return True
    except Exception as e:
        # Silently fail if cache clearing doesn't work
        return False

# Force cache clear on every deployment (without caching the function itself)
clear_all_caches()

# Import debugging and error handling
import sys
import os

# Show Python version and path for debugging
st.info(f"Python version: {sys.version}")
st.info(f"Python path: {sys.executable}")
st.info(f"Python 3.12 compatibility: ✅ Stable")

# Enhanced import handling for Streamlit Cloud
genai = None
import_success = False

# Method 1: Standard import
try:
    import google.generativeai as genai
    st.success("✅ google.generativeai imported successfully (Method 1)")
    import_success = True
except ImportError as e:
    st.warning(f"Method 1 failed: {e}")

# Method 2: Try with pip install first
if not import_success:
    try:
        import subprocess
        import sys
        st.info("🔄 Attempting to install google-generativeai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai==0.8.5"])
        import google.generativeai as genai
        st.success("✅ google.generativeai imported successfully (Method 2)")
        import_success = True
    except Exception as e:
        st.warning(f"Method 2 failed: {e}")

# Method 3: Try alternative import paths
if not import_success:
    try:
        from google.ai import generativeai as genai
        st.success("✅ google.ai.generativeai imported successfully (Method 3)")
        import_success = True
    except ImportError:
        try:
            import generativeai as genai
            st.success("✅ generativeai imported successfully (Method 4)")
            import_success = True
        except ImportError as e:
            st.error(f"❌ All import methods failed: {e}")

if not import_success:
    st.error("❌ Failed to import google-generativeai")
    st.error("Please ensure google-generativeai==0.8.5 is in requirements.txt")
    st.error("Streamlit Cloud should install it automatically during deployment")
    st.error("If the issue persists, try redeploying or check the deployment logs")
    st.stop()

try:
    from dotenv import load_dotenv
    load_dotenv()
    st.success("✅ python-dotenv imported successfully")
except ImportError as e:
    st.error(f"❌ Failed to import python-dotenv: {e}")
    st.stop()

try:
    # Import services
    from services.gemini_service import GeminiService
    from services.audio_service import AudioService
    from services.chatbot_service import ChatbotService
    
    # Import utility functions
    from utils.image_utils import resize_image, optimize_image_for_api
    
    # Initialize services
    gemini_service = GeminiService()
    audio_service = AudioService()
    chatbot_service = ChatbotService()
    
    st.success("✅ All services imported and initialized successfully")
    
except ImportError as e:
    st.error(f"❌ Service import error: {e}")
    st.error("Please check that all service files are present")
    st.error(f"Current working directory: {os.getcwd()}")
    st.error(f"Files in current directory: {os.listdir('.')}")
    st.stop()

# Page configuration with cache busting
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

# Simple cache busting for deployment
if 'deployment_time' not in st.session_state:
    st.session_state.deployment_time = time.time()

# Simple service initialization
def initialize_gemini():
    """Initialize Gemini service directly."""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("❌ GEMINI_API_KEY not found in secrets. Please add it in Streamlit Cloud settings.")
            st.info("Go to App Settings → Secrets and add: GEMINI_API_KEY = 'your_key_here'")
            st.stop()
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
        
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {str(e)}")
        st.stop()

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
    # Initialize Gemini
    model = initialize_gemini()
    
    st.success("✅ Gemini AI connected successfully!")
    
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
            
            # Debug options
            with st.expander("🔧 Developer Options"):
                debug_mode = st.checkbox("Show Debug Info", key="show_debug")
            
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

    # Main navigation tabs
    tab1, tab2 = st.tabs(["📷 Image Captioning", "💬 AI Chatbot"])
    
    with tab1:
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
                # Analysis options
                analysis_type = st.selectbox(
                    "Choose Analysis Type",
                    ["Standard Caption", "Location Analysis", "Product Analysis", "Comprehensive Analysis", "Text Extraction"],
                    help="Select the type of analysis you want to perform"
                )
                
                # Generate analysis button
                if st.button("🚀 Generate Analysis", type="primary", use_container_width=True):
                    with st.spinner(f"Generating {analysis_type.lower()}..."):
                        try:
                            # Optimize image for API
                            img_bytes = optimize_image_for_api(st.session_state.current_image, max_file_size_mb=2.0)
                            
                            # Generate analysis based on selected type
                            if analysis_type == "Standard Caption":
                                result = gemini_service.generate_caption(
                                    img_bytes, 
                                    style=caption_style.lower(),
                                    max_tokens=max_tokens,
                                    temperature=temperature
                                )
                            elif analysis_type == "Location Analysis":
                                location_result = gemini_service.identify_location(img_bytes)
                                result = location_result.get("location_analysis", "Location analysis failed")
                            elif analysis_type == "Product Analysis":
                                product_result = gemini_service.identify_product(img_bytes)
                                result = product_result.get("product_analysis", "Product analysis failed")
                            elif analysis_type == "Comprehensive Analysis":
                                comprehensive_result = gemini_service.comprehensive_analysis(img_bytes)
                                result = comprehensive_result.get("comprehensive_analysis", "Comprehensive analysis failed")
                            elif analysis_type == "Text Extraction":
                                text_result = gemini_service.extract_text_and_details(img_bytes)
                                result = text_result.get("text_analysis", "Text extraction failed")
                            else:
                                result = gemini_service.generate_caption(img_bytes, style=caption_style.lower())
                            
                            st.session_state.generated_caption = result
                            st.session_state.caption_generated = True
                            st.session_state.analysis_type = analysis_type
                            
                            # Success message
                            st.markdown(f'<div class="success-message">✅ {analysis_type} generated successfully!</div>', unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.markdown(f'<div class="error-message">❌ Error generating {analysis_type.lower()}: {str(e)}</div>', unsafe_allow_html=True)
            
                # Display and edit analysis result
                if 'generated_caption' in st.session_state and st.session_state.caption_generated:
                    analysis_type_display = st.session_state.get('analysis_type', 'Standard Caption')
                    
                    st.markdown('<div class="caption-box">', unsafe_allow_html=True)
                    
                    # Show analysis type
                    st.markdown(f"**Analysis Type:** {analysis_type_display}")
                    
                    # Editable result
                    edited_caption = st.text_area(
                        f"Edit {analysis_type_display} (optional)",
                        value=st.session_state.generated_caption,
                        height=200 if analysis_type_display != "Standard Caption" else 100,
                        help="You can edit the analysis result before generating audio"
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
                            # Detect audio format from file extension
                            _, ext = os.path.splitext(st.session_state.audio_file)
                            audio_format = 'audio/mp3' if ext.lower() == '.mp3' else 'audio/wav'
                            st.audio(audio_bytes, format=audio_format)
                        
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
                                # Detect audio format from file extension
                                _, ext = os.path.splitext(st.session_state.audio_file)
                                format_name = "MP3" if ext.lower() == '.mp3' else "WAV"
                                mime_type = "audio/mp3" if ext.lower() == '.mp3' else "audio/wav"
                                
                                st.download_button(
                                    label=f"🎵 Download Audio ({format_name})",
                                    data=audio_file.read(),
                                    file_name=f"vispio_audio_{int(time.time())}{ext}",
                                    mime=mime_type,
                                    use_container_width=True
                                )
            else:
                st.info("👆 Please upload an image to start generating captions.")
    
    with tab2:
        # Chatbot interface
        st.markdown("### 💬 AI Visual Assistant")
        st.write("Chat with AI about your images or ask general questions about visual content.")
        
        # Initialize chat history in session state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Chat interface
        chat_col1, chat_col2 = st.columns([1, 1], gap="large")
        
        with chat_col1:
            st.subheader("📷 Image for Chat")
            
            # File uploader for chat
            chat_uploaded_file = st.file_uploader(
                "Upload an image to chat about",
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'],
                help="Upload an image to ask questions about it",
                key="chat_uploader"
            )
            
            if chat_uploaded_file is not None:
                try:
                    chat_uploaded_file.seek(0)
                    chat_image = Image.open(chat_uploaded_file)
                    
                    # Basic validation
                    if chat_image.size[0] < 10 or chat_image.size[1] < 10:
                        st.error("Image is too small. Please upload a larger image.")
                    elif chat_image.size[0] * chat_image.size[1] > 100_000_000:
                        st.error("Image is too large. Please upload a smaller image.")
                    else:
                        # Resize and display image
                        display_chat_image = resize_image(chat_image, max_size=(400, 300))
                        st.image(display_chat_image, caption="Chat Image", use_container_width=True)
                        
                        # Store image in session state
                        st.session_state.chat_image = chat_image
                        st.session_state.chat_image_uploaded = True
                        
                        # Generate suggested questions
                        if st.button("💡 Get Suggested Questions", use_container_width=True):
                            with st.spinner("Generating suggested questions..."):
                                try:
                                    img_bytes = optimize_image_for_api(chat_image, max_file_size_mb=2.0)
                                    suggested_questions = chatbot_service.get_suggested_questions(img_bytes)
                                    st.session_state.suggested_questions = suggested_questions
                                except Exception as e:
                                    st.error(f"Error generating suggestions: {str(e)}")
                        
                        # Display suggested questions
                        if 'suggested_questions' in st.session_state:
                            st.markdown("**💡 Suggested Questions:**")
                            for i, question in enumerate(st.session_state.suggested_questions):
                                if st.button(f"❓ {question}", key=f"suggested_{i}", use_container_width=True):
                                    st.session_state.current_question = question
                                    st.rerun()
                        
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
        
        with chat_col2:
            st.subheader("💬 Chat Conversation")
            
            # Display chat history
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.chat_history[-10:]:  # Show last 10 messages
                    if message["role"] == "user":
                        st.markdown(f"**You:** {message['content']}")
                    else:
                        st.markdown(f"**AI:** {message['content']}")
                        st.markdown("---")
            
            # Chat input
            user_question = st.text_input(
                "Ask a question about the image or anything else:",
                placeholder="What do you see in this image?",
                key="chat_input",
                value=st.session_state.get('current_question', '')
            )
            
            # Clear the current question after setting it
            if 'current_question' in st.session_state:
                del st.session_state.current_question
            
            col_send, col_clear = st.columns([3, 1])
            
            with col_send:
                if st.button("💬 Send Message", type="primary", use_container_width=True):
                    if user_question.strip():
                        with st.spinner("AI is thinking..."):
                            try:
                                # Add user message to history
                                st.session_state.chat_history.append({
                                    "role": "user",
                                    "content": user_question
                                })
                                
                                # Generate AI response with intelligent routing
                                if 'chat_image_uploaded' in st.session_state and st.session_state.chat_image_uploaded:
                                    # Chat with image - detect question type for specialized analysis
                                    img_bytes = optimize_image_for_api(st.session_state.chat_image, max_file_size_mb=2.0)
                                    
                                    # Detect if this is a location or product question
                                    location_keywords = ['where', 'location', 'place', 'address', 'city', 'country', 'landmark', 'building', 'street']
                                    product_keywords = ['product', 'brand', 'price', 'buy', 'purchase', 'model', 'specification', 'what is this', 'identify']
                                    
                                    question_lower = user_question.lower()
                                    
                                    if any(keyword in question_lower for keyword in location_keywords):
                                        # Use specialized location analysis
                                        response = chatbot_service.analyze_location_context(img_bytes, user_question)
                                    elif any(keyword in question_lower for keyword in product_keywords):
                                        # Use specialized product analysis
                                        response = chatbot_service.analyze_product_context(img_bytes, user_question)
                                    else:
                                        # Use general chat with image
                                        response = chatbot_service.chat_with_image(
                                            img_bytes, 
                                            user_question,
                                            st.session_state.chat_history[:-1]  # Exclude the current message
                                        )
                                else:
                                    # Chat without image
                                    response = chatbot_service.chat_without_image(
                                        user_question,
                                        st.session_state.chat_history[:-1]  # Exclude the current message
                                    )
                                
                                # Add AI response to history
                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": response
                                })
                                
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Error getting AI response: {str(e)}")
                    else:
                        st.warning("Please enter a question or message.")
            
            with col_clear:
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    if 'suggested_questions' in st.session_state:
                        del st.session_state.suggested_questions
                    st.rerun()
    
    # Footer with About Us button
    st.markdown("---")
    
    # Center the about us button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🌟 About Us", type="secondary", use_container_width=True):
            st.session_state.show_about = True
            st.rerun()
    
    # About Us modal using proper Streamlit components
    if st.session_state.get('show_about', False):
        st.markdown("---")
        st.markdown("## 🌟 About Us")
        st.markdown("### Bringing Vision to Words with AI")
        
        st.write("At Vispio, we believe every image tells a story — and with the power of AI, we help you hear it.")
        
        st.write("Vispio isn't just a tool — it's your smart visual companion that can see, understand, and speak about the world around you. Whether it's a photo, a document, or a moment captured on your phone, our AI transforms images into meaningful descriptions — in both text and audio.")
        
        st.write("We're on a mission to make visual understanding seamless, accessible, and intelligent — for everyone.")
        
        st.markdown("### 🔍 What We Offer")
        
        st.markdown("**Image to Text Conversion**")
        st.write("Upload any image and instantly receive an accurate, natural-language description generated by AI.")
        
        st.markdown("**Image to Audio Narration**")
        st.write("Let your images speak. Our AI reads the description aloud using clear, human-like voice synthesis.")
        
        st.markdown("**Downloadable Transcripts & Audio Files**")
        st.write("Save what matters. You can download both the text and the audio files for future use or sharing.")
        
        st.markdown("**Fast, Secure, and Simple**")
        st.write("A smooth experience designed for privacy and speed — your data stays yours.")
        
        st.markdown("### 💡 Our Vision")
        st.write("To empower people with AI that sees and speaks, helping the world understand visuals through smart, voice-ready technology.")
        
        st.markdown("### 👥 Who We Are")
        st.write("We're passionate creators merging computer vision and AI to build tools that feel simple, powerful, and human-friendly.")
        
        st.markdown("---")
        st.markdown("<p style='text-align: center; font-weight: bold;'>Built with ❤️ by Devansh</p>", unsafe_allow_html=True)
        
        # Close button functionality
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
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
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chat_image_uploaded' not in st.session_state:
        st.session_state.chat_image_uploaded = False
    
    main()
