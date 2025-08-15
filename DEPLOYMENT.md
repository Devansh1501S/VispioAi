# Vispio Deployment Guide

## Streamlit Cloud Deployment

### Prerequisites
1. **Gemini API Key**: Get your API key from [Google AI Studio](https://aistudio.google.com/)
2. **GitHub Repository**: Push your code to a GitHub repository

### Deployment Steps

#### 1. Streamlit Cloud Setup
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `app.py`

#### 2. Environment Variables
In Streamlit Cloud, add these secrets in the app settings:

```toml
# .streamlit/secrets.toml (for Streamlit Cloud)
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

#### 3. Required Files
Ensure these files are in your repository:
- ✅ `requirements.txt` - Python dependencies
- ✅ `packages.txt` - System dependencies (ffmpeg for audio)
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `app.py` - Main application file

### Local Development

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Set Environment Variables
Create a `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

#### 3. Run Application
```bash
streamlit run app.py
```

### Alternative Deployment Options

#### Docker Deployment
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Heroku Deployment
1. Add `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Add `runtime.txt`:
```
python-3.11.9
```

### Environment Variables Required
- `GEMINI_API_KEY` - Google Gemini API key (Required)

### Troubleshooting

#### Common Issues
1. **Audio not working**: Ensure `ffmpeg` is installed (handled by `packages.txt`)
2. **API key errors**: Verify `GEMINI_API_KEY` is set correctly
3. **Import errors**: Check all dependencies are in `requirements.txt`

#### Memory Issues
If you encounter memory issues on Streamlit Cloud:
- Reduce image processing size in `utils/image_utils.py`
- Implement image caching strategies
- Consider upgrading to Streamlit Cloud Pro

### Performance Optimization
1. **Image Optimization**: Images are automatically resized and compressed
2. **Caching**: Services are cached using `@st.cache_resource`
3. **Memory Management**: Temporary files are cleaned up automatically

### Security Notes
- Never commit `.env` files with real API keys
- Use Streamlit Cloud secrets for production
- API keys are loaded securely via environment variables