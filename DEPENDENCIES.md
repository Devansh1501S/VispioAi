# 📦 Dependency Management Guide

## 🎯 Requirements Files Overview

### `requirements.txt` - Production Dependencies
**Use for**: Production deployment, Streamlit Cloud, Docker
```bash
pip install -r requirements.txt
```

**Contains**: Minimum required packages with flexible version ranges for compatibility.

### `requirements-lock.txt` - Locked Production Dependencies  
**Use for**: Exact production replication, CI/CD pipelines
```bash
pip install -r requirements-lock.txt
```

**Contains**: Exact versions from working production environment for reproducible builds.

### `requirements-dev.txt` - Development Dependencies
**Use for**: Local development, testing, code quality
```bash
pip install -r requirements-dev.txt
```

**Contains**: All production dependencies plus development tools (testing, linting, documentation).

## 🔧 Core Dependencies Explained

### Streamlit Framework
```
streamlit>=1.45.1          # Main web application framework
altair>=5.5.0              # Interactive visualizations
pydeck>=0.9.1              # Map visualizations
```

### AI and Machine Learning
```
google-generativeai>=0.8.5 # Google Gemini API for image analysis
numpy>=1.26.4              # Numerical computing foundation
```

### Image Processing
```
Pillow>=10.3.0             # Image manipulation and processing
```

### Audio Processing
```
gtts>=2.5.4                # Google Text-to-Speech
pydub>=0.25.1              # Audio file manipulation
pygame>=2.6.0              # Audio playback capabilities
```

### Utilities
```
python-dotenv>=1.0.1       # Environment variable management
requests>=2.31.0           # HTTP requests
typing-extensions>=4.13.0  # Enhanced type hints
packaging>=24.0            # Version parsing utilities
```

## 🚀 Installation Instructions

### For Production Deployment
```bash
# Standard installation
pip install -r requirements.txt

# Or for exact version matching
pip install -r requirements-lock.txt
```

### For Development
```bash
# Install development environment
pip install -r requirements-dev.txt

# Or step by step
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### For Streamlit Cloud
1. Use `requirements.txt` (automatically detected)
2. Ensure `packages.txt` is present for system dependencies
3. Set environment variables in Streamlit Cloud secrets

## 🔄 Updating Dependencies

### Check for Updates
```bash
pip list --outdated
```

### Update Specific Package
```bash
pip install --upgrade package-name
```

### Regenerate Lock File
```bash
pip freeze > requirements-lock.txt
```

### Test After Updates
```bash
python service_health_check.py
python integration_test.py
```

## 🐳 Docker Requirements

### Dockerfile Dependencies
```dockerfile
# Use requirements-lock.txt for reproducible builds
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt
```

### System Dependencies (packages.txt)
```
ffmpeg              # Audio processing
libsndfile1         # Audio file support
```

## 🔍 Dependency Analysis

### Security Scanning
```bash
pip install safety
safety check -r requirements.txt
```

### License Checking
```bash
pip install pip-licenses
pip-licenses --format=table
```

### Dependency Tree
```bash
pip install pipdeptree
pipdeptree
```

## ⚠️ Common Issues and Solutions

### Issue: `pygame` Installation Fails
**Solution**: 
```bash
# Windows
pip install pygame --pre

# Linux/Mac
sudo apt-get install python3-dev
pip install pygame
```

### Issue: `pydub` Audio Processing Fails
**Solution**: Install ffmpeg system dependency
```bash
# Windows (using winget)
winget install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Issue: `Pillow` Import Errors
**Solution**: Reinstall with proper dependencies
```bash
pip uninstall Pillow
pip install Pillow --upgrade
```

### Issue: Streamlit Cache Problems
**Solution**: Clear cache and reinstall
```bash
python clear_cache_and_test.py
pip install --force-reinstall streamlit
```

## 📊 Dependency Compatibility Matrix

| Python Version | Streamlit | Google-GenAI | Status |
|---------------|-----------|--------------|---------|
| 3.8           | ✅ 1.45+  | ✅ 0.8+      | Supported |
| 3.9           | ✅ 1.45+  | ✅ 0.8+      | Supported |
| 3.10          | ✅ 1.45+  | ✅ 0.8+      | Recommended |
| 3.11          | ✅ 1.45+  | ✅ 0.8+      | Recommended |
| 3.12          | ✅ 1.45+  | ✅ 0.8+      | Latest |

## 🎯 Best Practices

### Version Pinning Strategy
- **Production**: Use `requirements-lock.txt` for exact versions
- **Development**: Use `requirements.txt` for flexibility
- **CI/CD**: Use locked versions for reproducible builds

### Regular Maintenance
1. **Weekly**: Check for security updates
2. **Monthly**: Review and update non-breaking versions
3. **Quarterly**: Major version updates with full testing

### Testing After Updates
```bash
# Run full test suite
python service_health_check.py
python integration_test.py
python test_analysis.py

# Test specific functionality
streamlit run app.py
```

## 📝 Adding New Dependencies

### Process
1. Add to `requirements.txt` with minimum version
2. Test thoroughly with `integration_test.py`
3. Update `requirements-lock.txt` with `pip freeze`
4. Update this documentation
5. Test deployment on Streamlit Cloud

### Example
```bash
# Add new dependency
pip install new-package>=1.0.0

# Test integration
python integration_test.py

# Update lock file
pip freeze > requirements-lock.txt

# Update requirements.txt
echo "new-package>=1.0.0" >> requirements.txt
```

---

## 🎉 Ready for Deployment

With these dependency files, your Vispio application is ready for:
- ✅ Local development
- ✅ Production deployment  
- ✅ Streamlit Cloud hosting
- ✅ Docker containerization
- ✅ CI/CD pipelines