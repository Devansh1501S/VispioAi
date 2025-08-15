import streamlit as st
import os
import io
from PIL import Image
import time

# Page configuration
st.set_page_config(
    page_title="Vispio - AI Image Captioning",
    page_icon="logo.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🎯 Vispio - AI Image Analysis")
    st.markdown("**Let AI Speak Your Pictures**")
    
    # Check if google-generativeai is available
    try:
        import google.generativeai as genai
        st.success("✅ Google Generative AI is available!")
        
        # Initialize Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("❌ GEMINI_API_KEY not found. Please add it in Streamlit Cloud settings.")
            st.info("Go to App Settings → Secrets and add: GEMINI_API_KEY = 'your_key_here'")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            st.success("✅ Gemini AI connected successfully!")
            
    except ImportError:
        st.warning("⚠️ Google Generative AI not available")
        st.info("This is a fallback version. Please ensure google-generativeai is installed.")
    
    # Basic image upload functionality
    uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            if st.button("🚀 Analyze Image"):
                st.info("Image analysis requires Google Generative AI to be properly installed.")
                st.info("Please check the requirements.txt file and redeploy.")
                
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    st.info("🎉 Basic version working! Full features will be available once Google Generative AI is properly installed.")

if __name__ == "__main__":
    main() 