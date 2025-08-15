#!/usr/bin/env python3
"""
Pre-deployment check for Streamlit Cloud
"""

import os
import sys
from pathlib import Path

def check_deployment_readiness():
    """Check if the project is ready for Streamlit Cloud deployment."""
    
    print("🚀 Streamlit Cloud Deployment Readiness Check")
    print("=" * 60)
    
    checks = []
    
    # 1. Check .env file safety
    print("\n🔐 Checking Environment File Security...")
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
            if 'AIza' in env_content and 'your_' not in env_content:
                checks.append(("❌", ".env contains real API key - SECURITY RISK!"))
            else:
                checks.append(("✅", ".env contains placeholder only"))
    else:
        checks.append(("⚠️", ".env file not found"))
    
    # 2. Check .gitignore
    print("\n🚫 Checking .gitignore...")
    gitignore_file = Path('.gitignore')
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                checks.append(("✅", ".env is in .gitignore"))
            else:
                checks.append(("❌", ".env NOT in .gitignore - will expose secrets!"))
    else:
        checks.append(("❌", ".gitignore file missing"))
    
    # 3. Check requirements.txt
    print("\n📦 Checking requirements.txt...")
    req_file = Path('requirements.txt')
    if req_file.exists():
        with open(req_file, 'r') as f:
            req_content = f.read()
            required_packages = [
                'streamlit', 'google-generativeai', 'gtts', 
                'pydub', 'pygame', 'Pillow', 'python-dotenv'
            ]
            missing_packages = []
            for package in required_packages:
                if package not in req_content:
                    missing_packages.append(package)
            
            if not missing_packages:
                checks.append(("✅", "All required packages in requirements.txt"))
            else:
                checks.append(("❌", f"Missing packages: {missing_packages}"))
    else:
        checks.append(("❌", "requirements.txt file missing"))
    
    # 4. Check packages.txt
    print("\n🔧 Checking packages.txt...")
    pkg_file = Path('packages.txt')
    if pkg_file.exists():
        with open(pkg_file, 'r') as f:
            pkg_content = f.read()
            if 'ffmpeg' in pkg_content:
                checks.append(("✅", "System packages configured"))
            else:
                checks.append(("⚠️", "ffmpeg not in packages.txt - audio may be limited"))
    else:
        checks.append(("⚠️", "packages.txt missing - audio may be limited"))
    
    # 5. Check main app file
    print("\n📄 Checking main app file...")
    app_file = Path('app.py')
    if app_file.exists():
        checks.append(("✅", "app.py exists"))
    else:
        checks.append(("❌", "app.py missing"))
    
    # 6. Check for hardcoded secrets
    print("\n🔍 Scanning for hardcoded secrets...")
    secret_found = False
    for py_file in Path('.').rglob('*.py'):
        if py_file.name == 'deployment_check.py':
            continue
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if 'AIza' in content and 'your_' not in content:
                    checks.append(("❌", f"Potential API key in {py_file}"))
                    secret_found = True
        except:
            pass
    
    if not secret_found:
        checks.append(("✅", "No hardcoded secrets found"))
    
    return checks

def print_deployment_instructions(checks):
    """Print deployment instructions based on check results."""
    
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT READINESS REPORT")
    print("=" * 60)
    
    passed = 0
    failed = 0
    warnings = 0
    
    for status, message in checks:
        print(f"{status} {message}")
        if status == "✅":
            passed += 1
        elif status == "❌":
            failed += 1
        else:
            warnings += 1
    
    print(f"\n📈 Summary: {passed} passed, {failed} failed, {warnings} warnings")
    
    if failed > 0:
        print("\n🚨 DEPLOYMENT BLOCKED - Fix issues above first!")
        print("\n🔧 Quick Fixes:")
        print("1. Remove real API keys from all files")
        print("2. Ensure .env is in .gitignore")
        print("3. Update requirements.txt if needed")
        print("4. Run: python security_check.py")
        return False
    
    elif warnings > 0:
        print("\n⚠️ DEPLOYMENT READY with warnings")
        print("You can deploy, but consider fixing warnings for better experience")
    else:
        print("\n🎉 DEPLOYMENT READY!")
    
    print("\n🚀 Next Steps for Streamlit Cloud:")
    print("1. Push code to GitHub: git push origin main")
    print("2. Go to: https://share.streamlit.io")
    print("3. Deploy your app")
    print("4. Add API key in Streamlit Cloud Secrets:")
    print('   GEMINI_API_KEY = "your_actual_api_key_here"')
    print("5. Test your deployed app!")
    
    return True

def generate_secrets_template():
    """Generate a template for Streamlit Cloud secrets."""
    
    print("\n📝 Streamlit Cloud Secrets Template:")
    print("-" * 40)
    print("Copy this into your Streamlit Cloud Secrets section:")
    print()
    print("```toml")
    print('GEMINI_API_KEY = "your_actual_new_api_key_here"')
    print('ENVIRONMENT = "production"')
    print("```")
    print()
    print("⚠️ Replace 'your_actual_new_api_key_here' with your real API key!")

def main():
    """Main deployment check function."""
    
    checks = check_deployment_readiness()
    ready = print_deployment_instructions(checks)
    
    if ready:
        generate_secrets_template()
    
    return ready

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)