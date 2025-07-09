# Vispio - AI Image Captioning Application

## Overview

Vispio is a Streamlit-based web application that provides AI-powered image captioning capabilities. The application allows users to upload images and receive detailed, AI-generated captions using Google's Gemini Vision API. Additionally, it offers text-to-speech functionality to convert the generated captions into audio format.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular service-oriented architecture with clear separation of concerns:

- **Frontend**: Streamlit-based web interface providing an intuitive user experience
- **Backend Services**: Modular Python services handling core functionality
- **AI Integration**: Google Gemini Vision API for image analysis and caption generation
- **Audio Processing**: Text-to-speech capabilities using Google TTS (gTTS) and pygame
- **Image Processing**: PIL-based image validation and manipulation utilities

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and UI orchestration
- **Responsibilities**: 
  - Streamlit page configuration and custom styling
  - Service initialization with caching
  - User interface layout and interaction handling
- **Design Decision**: Uses Streamlit's caching mechanism to initialize services once for performance optimization

### 2. Gemini Service (`services/gemini_service.py`)
- **Purpose**: Interface with Google Gemini Vision API
- **Key Features**:
  - Multiple caption styles (descriptive, creative, technical, simple)
  - Configurable generation parameters (max_tokens, temperature)
  - Error handling and logging
- **Design Decision**: Encapsulates all Gemini API interactions in a dedicated service for maintainability and testability

### 3. Audio Service (`services/audio_service.py`)
- **Purpose**: Text-to-speech conversion and audio playback
- **Key Features**:
  - Multi-language support
  - Adjustable speech speed
  - Multiple output formats (WAV, MP3)
  - Pygame-based audio playback
- **Design Decision**: Uses gTTS for cloud-based TTS with pygame for local playback, providing flexibility and quality

### 4. Image Utilities (`utils/image_utils.py`)
- **Purpose**: Image validation and processing
- **Key Features**:
  - Comprehensive image validation (size, format, dimensions)
  - Image resizing capabilities
  - Support for multiple image formats
- **Design Decision**: Separate utility module for image operations to promote code reuse and testing

## Data Flow

1. **Image Upload**: User uploads image through Streamlit interface
2. **Validation**: Image is validated for format, size, and quality using PIL
3. **Processing**: Valid images are processed and sent to Gemini Vision API
4. **Caption Generation**: Gemini API analyzes image and generates caption based on selected style
5. **Audio Conversion**: Generated caption is optionally converted to speech using gTTS
6. **Output**: Results are displayed in the web interface with optional audio playback

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for rapid UI development
- **Google Generative AI**: Official Google client for Gemini API access
- **Pillow (PIL)**: Image processing and validation
- **gTTS**: Google Text-to-Speech for audio generation
- **pygame**: Audio playback functionality
- **pydub**: Audio processing and format conversion

### Environment Variables
- **GEMINI_API_KEY**: Required for Google Gemini Vision API authentication

## Deployment Strategy

The application is designed for cloud deployment with the following considerations:

### Environment Setup
- Requires Python 3.7+ environment
- All dependencies managed through standard Python package management
- Environment variables for API key configuration

### Scalability Considerations
- Service-based architecture allows for independent scaling of components
- Caching mechanisms reduce redundant API calls
- Modular design supports easy feature additions and modifications

### Security
- API keys managed through environment variables
- Input validation for uploaded images
- Error handling prevents information leakage

The architecture prioritizes maintainability, scalability, and user experience while leveraging cloud-based AI services for core functionality.