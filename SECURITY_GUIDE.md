# 🔒 Security Guide - API Key Management

## 🚨 IMMEDIATE ACTION REQUIRED

If your API key was exposed, follow these steps **RIGHT NOW**:

### 1. **Revoke Exposed API Key**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Find your current API key (starts with `AIza...`)
3. Click **"Delete"** or **"Revoke"** immediately
4. Generate a new API key

### 2. **Generate New API Key**
1. In Google AI Studio, click **"Create API Key"**
2. Copy the new key (starts with `AIza...`)
3. **DO NOT** paste it directly in any file

### 3. **Secure the New API Key**
```bash
# Edit your .env file (this file is NOT committed to Git)
nano .env

# Replace the placeholder with your NEW key:
GEMINI_API_KEY=your_new_api_key_here
```

## 🛡️ Security Best Practices

### ✅ What We've Already Secured

1. **`.env` in .gitignore** - Your .env file will never be committed
2. **`.env.example`** - Template file with placeholder (safe to commit)
3. **Environment variable loading** - App reads from environment, not hardcoded

### 🔒 How to Safely Manage API Keys

#### For Local Development:
```bash
# 1. Edit .env file (never committed)
GEMINI_API_KEY=your_actual_new_api_key

# 2. The app automatically loads from .env
python app.py
```

#### For Streamlit Cloud Deployment:
```toml
# In Streamlit Cloud App Settings > Secrets
GEMINI_API_KEY = "your_actual_new_api_key"
```

#### For Docker Deployment:
```bash
# Pass as environment variable
docker run -e GEMINI_API_KEY=your_actual_new_api_key your-app
```

#### For Heroku Deployment:
```bash
# Set config var
heroku config:set GEMINI_API_KEY=your_actual_new_api_key
```

## 🚫 What NEVER to Do

### ❌ NEVER put API keys in:
- Source code files (.py, .js, etc.)
- Configuration files committed to Git
- README files or documentation
- Comments in code
- Environment files committed to Git (.env)
- Public repositories
- Screenshots or videos
- Chat messages or emails

### ❌ NEVER commit files containing:
```bash
# These patterns expose API keys
GEMINI_API_KEY=AIza...
api_key = "AIza..."
API_KEY: AIza...
```

## ✅ Secure Patterns

### ✅ Always use environment variables:
```python
# ✅ CORRECT - Read from environment
import os
api_key = os.environ.get("GEMINI_API_KEY")

# ❌ WRONG - Hardcoded key
api_key = "AIzaSyC1Qka73olSAgCpIor7EiufDXrJbAc322c"
```

### ✅ Always validate environment setup:
```python
# ✅ CORRECT - Validate key exists
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")
```

## 🔍 Security Checklist

### Before Every Commit:
- [ ] Check no API keys in code: `git diff --cached`
- [ ] Verify .env is in .gitignore
- [ ] Run security scan: `python security_check.py`

### Before Every Deployment:
- [ ] API keys set in deployment environment
- [ ] No hardcoded secrets in code
- [ ] Environment variables properly configured

### Regular Security Maintenance:
- [ ] Rotate API keys every 90 days
- [ ] Monitor API key usage in Google Cloud Console
- [ ] Review access logs regularly
- [ ] Update dependencies for security patches

## 🛠️ Security Tools

### Git Hooks (Prevent Accidental Commits)
```bash
# Install pre-commit hook
pip install pre-commit
pre-commit install

# This will scan for secrets before each commit
```

### Manual Security Scan
```bash
# Check for exposed secrets
python security_check.py

# Scan git history for leaked keys
git log --all --full-history -- .env
```

## 🚨 If API Key is Compromised

### Immediate Response (within 5 minutes):
1. **Revoke the key** in Google AI Studio
2. **Generate new key**
3. **Update all deployments** with new key
4. **Monitor usage** for unauthorized access

### Investigation (within 1 hour):
1. Check Google Cloud Console for unusual API usage
2. Review git history: `git log --oneline --all`
3. Check if key was used maliciously
4. Document the incident

### Prevention (within 24 hours):
1. Implement git hooks to prevent future exposure
2. Add automated security scanning
3. Train team on security practices
4. Review and update security procedures

## 📱 Platform-Specific Security

### Streamlit Cloud
```toml
# In App Settings > Secrets (encrypted storage)
GEMINI_API_KEY = "your_key_here"
```

### GitHub Actions
```yaml
# In Repository Settings > Secrets
env:
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

### Docker
```dockerfile
# Use build args (not in final image)
ARG GEMINI_API_KEY
ENV GEMINI_API_KEY=$GEMINI_API_KEY
```

## 🎯 Quick Security Commands

### Check for exposed keys:
```bash
# Scan current files
grep -r "AIza" . --exclude-dir=.git

# Check git history
git log --all --full-history -p | grep -i "AIza"
```

### Clean git history (if key was committed):
```bash
# Remove sensitive data from git history
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch .env' \
--prune-empty --tag-name-filter cat -- --all
```

---

## 🎉 You're Now Secure!

After following this guide:
- ✅ Old API key revoked
- ✅ New API key secured in .env
- ✅ .env never committed to Git
- ✅ Deployment uses environment variables
- ✅ Security best practices implemented

**Remember**: API keys are like passwords - treat them with the same level of security!