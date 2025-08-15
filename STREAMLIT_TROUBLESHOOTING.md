# 🔧 Streamlit Cloud Troubleshooting Guide

## 🚨 Common Error: ModuleNotFoundError for google.generativeai

### The Error You're Seeing:
```
ModuleNotFoundError: This app has encountered an error. 
File "/mount/src/vispio/services/gemini_service.py", line 4, in <module>
    import google.generativeai as genai
```

### 🔧 **SOLUTION 1: Update requirements.txt (RECOMMENDED)**

I've already updated your `requirements.txt` with fixed versions. The issue is that Streamlit Cloud sometimes has trouble with the latest versions of Google packages.

**Action Required:**
1. Commit and push the updated `requirements.txt`
2. Streamlit Cloud will automatically redeploy
3. The fixed versions should resolve the import issue

```bash
git add requirements.txt
git commit -m "fix: Update requirements.txt with fixed versions for Streamlit Cloud"
git push origin main
```

### 🔧 **SOLUTION 2: Alternative Requirements (If Solution 1 Fails)**

If the error persists, try this minimal requirements.txt:

```txt
streamlit
google-generativeai
gtts
pydub
pygame
Pillow
python-dotenv
requests
numpy
```

### 🔧 **SOLUTION 3: Force Reinstall Dependencies**

In Streamlit Cloud:
1. Go to your app settings
2. Click "Reboot app"
3. This forces a fresh install of all dependencies

### 🔧 **SOLUTION 4: Check Python Version**

Ensure your app is using Python 3.9+ by adding a `runtime.txt` file:

```txt
python-3.11
```

## 🚨 Other Common Streamlit Cloud Issues

### Issue: "Secrets not found"
**Solution:**
1. Go to app Settings > Secrets
2. Add your API key in TOML format:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key"
   ```
3. Save and restart

### Issue: "Audio processing fails"
**Solution:**
- This is expected on Streamlit Cloud
- App will fallback to MP3 format
- Ensure `packages.txt` contains `ffmpeg`

### Issue: "App is slow to load"
**Solution:**
- First deployment takes 5-10 minutes
- Subsequent loads are faster
- This is normal Streamlit Cloud behavior

### Issue: "Memory errors"
**Solution:**
- Reduce image processing size
- Use `@st.cache_resource` for services
- Clear temporary files regularly

## 🔍 Debugging Steps

### 1. Check Streamlit Cloud Logs
1. Go to your app dashboard
2. Click "Manage app"
3. View real-time logs for specific errors

### 2. Test Locally First
```bash
# Test your app locally before deploying
streamlit run app.py
```

### 3. Verify Dependencies
```bash
# Run this to check all imports work
python fix_imports.py
```

### 4. Check Git Repository
- Ensure all files are committed
- Verify `requirements.txt` is in root directory
- Check that `packages.txt` exists

## 🚀 Deployment Best Practices

### ✅ Before Every Deployment:
1. Test locally: `streamlit run app.py`
2. Check requirements: `python deployment_check.py`
3. Verify security: `python security_check.py`
4. Commit all changes: `git push origin main`

### ✅ After Deployment:
1. Check logs for errors
2. Test all app features
3. Verify API key is working
4. Test on mobile devices

## 📞 Getting Help

### If Issues Persist:
1. **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
2. **Check Status**: [status.streamlit.io](https://status.streamlit.io)
3. **Documentation**: [docs.streamlit.io](https://docs.streamlit.io)

### Common Solutions Repository:
- Try different Python versions (3.9, 3.10, 3.11)
- Use exact package versions instead of ranges
- Check for package conflicts
- Verify all imports work locally

## 🎯 Quick Fix Commands

### Update and Redeploy:
```bash
# Update requirements with fixed versions
git add requirements.txt
git commit -m "fix: Streamlit Cloud compatibility"
git push origin main
```

### Force Clean Deployment:
1. Delete app from Streamlit Cloud
2. Redeploy from scratch
3. Add secrets again

### Test Import Fix:
```bash
python -c "import google.generativeai; print('✅ Import successful')"
```

---

## 🎉 Success Indicators

Your deployment is successful when:
- ✅ App loads without ModuleNotFoundError
- ✅ Image upload works
- ✅ All 5 analysis types function
- ✅ API key is properly loaded from secrets
- ✅ No critical errors in logs

**The updated requirements.txt should fix your import issue! 🚀**