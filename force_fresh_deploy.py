#!/usr/bin/env python3
"""
Force fresh Streamlit Cloud deployment by busting cache
"""

import os
import re
import time
from datetime import datetime

def update_deployment_version():
    """Update deployment version in app.py to force cache bust."""
    
    app_file = 'app.py'
    
    if not os.path.exists(app_file):
        print("❌ app.py not found")
        return False
    
    # Read current content
    with open(app_file, 'r') as f:
        content = f.read()
    
    # Generate new version
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_version = f"1.0.{int(time.time() % 10000)}"
    
    # Update version
    pattern = r'DEPLOYMENT_VERSION = "[^"]*"'
    replacement = f'DEPLOYMENT_VERSION = "{new_version}"'
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        
        with open(app_file, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated deployment version to: {new_version}")
        return True
    else:
        print("⚠️ DEPLOYMENT_VERSION not found in app.py")
        return False

def update_requirements_cache_bust():
    """Add cache bust comment to requirements.txt."""
    
    req_file = 'requirements.txt'
    
    if not os.path.exists(req_file):
        print("❌ requirements.txt not found")
        return False
    
    # Read current content
    with open(req_file, 'r') as f:
        lines = f.readlines()
    
    # Generate cache bust comment
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M")
    cache_bust = f"# Cache bust: {timestamp} - Force fresh Streamlit Cloud deployment\n"
    
    # Remove old cache bust comments
    lines = [line for line in lines if not line.startswith("# Cache bust:")]
    
    # Add new cache bust at the top
    lines.insert(0, cache_bust)
    
    # Write back
    with open(req_file, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Added cache bust comment: {timestamp}")
    return True

def update_streamlit_config():
    """Update Streamlit config with timestamp to force rebuild."""
    
    config_dir = '.streamlit'
    config_file = os.path.join(config_dir, 'config.toml')
    
    # Ensure directory exists
    os.makedirs(config_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    
    config_content = f"""[server]
headless = true
enableCORS = false
enableXsrfProtection = false
# Force rebuild timestamp: {timestamp}

[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false

[client]
showErrorDetails = false
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Updated Streamlit config with timestamp: {timestamp}")
    return True

def main():
    """Main function to force fresh deployment."""
    
    print("🔄 Force Fresh Streamlit Cloud Deployment")
    print("=" * 50)
    
    success_count = 0
    
    # Update deployment version
    if update_deployment_version():
        success_count += 1
    
    # Update requirements cache bust
    if update_requirements_cache_bust():
        success_count += 1
    
    # Update Streamlit config
    if update_streamlit_config():
        success_count += 1
    
    print("\n" + "=" * 50)
    
    if success_count == 3:
        print("🎉 All cache bust mechanisms updated!")
        print("\n🚀 Next steps:")
        print("1. git add .")
        print("2. git commit -m 'feat: Force fresh Streamlit Cloud deployment'")
        print("3. git push origin main")
        print("\n💡 Your Streamlit Cloud app will now boot completely fresh!")
    else:
        print(f"⚠️ {success_count}/3 updates successful. Check errors above.")

if __name__ == "__main__":
    main()