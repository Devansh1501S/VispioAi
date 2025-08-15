# 🔐 Streamlit Cloud Secrets Setup - Visual Guide

## 📍 Where to Add Your API Key in Streamlit Cloud

### Method 1: During Initial Setup
```
1. Deploy app → App fails (expected)
2. Go to app dashboard
3. Click "Settings" or "⚙️" 
4. Click "Secrets" tab
5. Add your secrets
```

### Method 2: After Deployment
```
1. Visit: https://share.streamlit.io
2. Find your app in the dashboard
3. Click the three dots "..." menu
4. Select "Settings"
5. Go to "Secrets" section
```

## 📝 Exact Format for Secrets

Copy and paste this into the Streamlit Cloud Secrets box:

```toml
GEMINI_API_KEY = "AIza_your_new_api_key_here"
```

**Important Notes:**
- Use your NEW API key (not the old exposed one)
- Keep the quotes around the key
- Use exact variable name: `GEMINI_API_KEY`
- TOML format (not JSON or other formats)

## 🔄 Complete Deployment Workflow

### 1. Prepare Your Repository
```bash
# Make sure .env has placeholder (not real key)
echo 'GEMINI_API_KEY=your_gemini_api_key_here' > .env

# Commit and push
git add .
git commit -m "feat: Ready for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Choose your GitHub repository
4. Set main file: `app.py`
5. Click "Deploy"

### 3. Add Secrets (While App is Failing)
1. App will show error: "GEMINI_API_KEY environment variable is required"
2. Click "Settings" in your app dashboard
3. Go to "Secrets" tab
4. Paste your API key in TOML format:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key"
   ```
5. Click "Save"

### 4. Verify Deployment
- App should restart automatically
- Check that all features work
- Test image upload and analysis

## 🚨 Common Mistakes to Avoid

### ❌ Wrong Format:
```toml
# DON'T do this:
GEMINI_API_KEY: your_key_here          # Wrong syntax
"GEMINI_API_KEY" = your_key_here       # Missing quotes on value
GEMINI_API_KEY = your_key_here         # Missing quotes on value
```

### ✅ Correct Format:
```toml
# DO this:
GEMINI_API_KEY = "your_actual_api_key_here"
```

### ❌ Wrong Variable Name:
```toml
# DON'T do this:
API_KEY = "your_key"           # Wrong name
GOOGLE_API_KEY = "your_key"    # Wrong name
gemini_api_key = "your_key"    # Wrong case
```

### ✅ Correct Variable Name:
```toml
# DO this:
GEMINI_API_KEY = "your_key"    # Exact match with code
```

## 🔍 Troubleshooting Secrets

### If App Still Shows API Key Error:

1. **Check Secret Name**: Must be exactly `GEMINI_API_KEY`
2. **Check Format**: Must be TOML format with quotes
3. **Restart App**: Click "Reboot" in app settings
4. **Check Logs**: Look for specific error messages

### Verify Secrets Are Working:
```python
# This code in your app will help debug:
import os
import streamlit as st

# Add this temporarily to check if secret is loaded
if st.sidebar.button("Debug: Check API Key"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        st.success(f"API Key loaded: {api_key[:10]}...")
    else:
        st.error("API Key not found in environment")
```

## 📱 Mobile-Friendly Deployment

Your Streamlit app will automatically work on mobile devices:
- Responsive design included
- Touch-friendly interface
- Mobile image upload supported

## 🎯 Quick Deployment Checklist

Before clicking "Deploy":
- [ ] Real API key NOT in any committed files
- [ ] `.env` contains placeholder only
- [ ] `requirements.txt` is up to date
- [ ] `packages.txt` exists with system dependencies
- [ ] Code is pushed to GitHub main branch

After deployment:
- [ ] Add API key to Streamlit Cloud secrets
- [ ] Test all app features
- [ ] Verify no errors in logs
- [ ] Share your app URL!

## 🌟 Your App URL

After successful deployment, your app will be available at:
```
https://your-app-name-your-username.streamlit.app
```

Share this URL with anyone - your Vispio AI Image Captioning app is now live! 🎉