# 🚀 Streamlit Cloud Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Before You Deploy:
- [ ] API key removed from all code files
- [ ] `.env` file in `.gitignore`
- [ ] `requirements.txt` updated
- [ ] `packages.txt` created for system dependencies
- [ ] Code pushed to GitHub

## 🔐 Step-by-Step Deployment with Secrets

### Step 1: Initial Deployment
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account
4. Select your repository: `your-username/vispio-ai-image-captioning`
5. Set main file path: `app.py`
6. Click **"Deploy!"**

**Note**: The app will initially fail with an API key error - this is expected!

### Step 2: Add Secrets (API Key)
1. In your Streamlit Cloud dashboard, find your app
2. Click the **"⚙️ Settings"** button (or three dots menu)
3. Go to **"Secrets"** tab
4. Add your secrets in TOML format:

```toml
# Paste this in the Secrets section:
GEMINI_API_KEY = "your_actual_new_api_key_here"

# Optional: Add other environment variables
ENVIRONMENT = "production"
```

### Step 3: Restart Your App
1. After adding secrets, click **"Save"**
2. Your app will automatically restart
3. The app should now work with your API key!

## 📁 Required Files for Deployment

### 1. `requirements.txt` ✅ (Already created)
```txt
streamlit>=1.45.1
google-generativeai>=0.8.5
gtts>=2.5.4
pydub>=0.25.1
pygame>=2.6.0
Pillow>=10.3.0
python-dotenv>=1.0.1
requests>=2.31.0
numpy>=1.26.4
typing-extensions>=4.13.0
packaging>=24.0
```

### 2. `packages.txt` ✅ (Already created)
```txt
ffmpeg
libsndfile1
```

### 3. `.streamlit/config.toml` ✅ (Already created)
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false

[client]
showErrorDetails = false
```

## 🔧 Troubleshooting Common Issues

### Issue: "GEMINI_API_KEY environment variable is required"
**Solution**: 
1. Check secrets are properly added in Streamlit Cloud
2. Ensure the key name matches exactly: `GEMINI_API_KEY`
3. Restart the app after adding secrets

### Issue: "Module not found" errors
**Solution**: 
1. Check `requirements.txt` includes all dependencies
2. Verify package names are correct
3. Check for typos in package names

### Issue: Audio processing fails
**Solution**: 
1. Ensure `packages.txt` includes `ffmpeg`
2. The app will fallback to MP3 format if ffmpeg fails
3. This is normal and expected behavior

### Issue: App is slow to start
**Solution**: 
1. This is normal for first deployment
2. Streamlit Cloud needs to install dependencies
3. Subsequent starts will be faster

## 📊 Monitoring Your Deployment

### Check App Health:
1. **Logs**: View real-time logs in Streamlit Cloud dashboard
2. **Metrics**: Monitor app usage and performance
3. **Errors**: Check for any runtime errors

### Performance Tips:
1. **Caching**: App uses `@st.cache_resource` for service initialization
2. **Image Optimization**: Images are automatically resized
3. **Memory Management**: Temporary files are cleaned up

## 🔄 Updating Your Deployment

### Code Updates:
1. Push changes to your GitHub repository
2. Streamlit Cloud automatically redeploys
3. No need to restart manually

### Secrets Updates:
1. Go to app settings in Streamlit Cloud
2. Update secrets in the Secrets tab
3. App will restart automatically

### Dependency Updates:
1. Update `requirements.txt` in your repository
2. Push changes to GitHub
3. Streamlit Cloud will reinstall dependencies

## 🌐 Custom Domain (Optional)

### Using Custom Domain:
1. Upgrade to Streamlit Cloud Pro (if needed)
2. Go to app settings
3. Add your custom domain
4. Update DNS settings as instructed

## 📱 Sharing Your App

### Public Sharing:
- Your app URL: `https://your-app-name.streamlit.app`
- Share this URL with anyone
- No authentication required by default

### Private Sharing:
- Upgrade to Streamlit Cloud Pro for private apps
- Control access with email invitations

## 🔒 Security Best Practices

### ✅ What's Secure:
- API keys stored in Streamlit Cloud secrets (encrypted)
- `.env` file not committed to repository
- Secrets not visible in logs or code

### ⚠️ Additional Security:
- Regularly rotate API keys (every 90 days)
- Monitor API usage in Google Cloud Console
- Use strong, unique passwords for GitHub and Streamlit accounts

## 🎯 Success Checklist

After deployment, verify:
- [ ] App loads without errors
- [ ] Image upload works
- [ ] All 5 analysis types function
- [ ] Audio generation works (MP3 format)
- [ ] Chatbot responds correctly
- [ ] No API key errors in logs

## 📞 Support Resources

### If You Need Help:
1. **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
2. **Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
3. **GitHub Issues**: Create issues in your repository
4. **Google AI Studio**: [aistudio.google.com](https://aistudio.google.com)

---

## 🎉 You're Ready to Deploy!

Your Vispio app is now ready for production deployment on Streamlit Cloud with:
- ✅ Secure API key management
- ✅ All dependencies configured
- ✅ System packages included
- ✅ Error handling implemented
- ✅ Performance optimized