#!/usr/bin/env python3
"""
Quick cache bust for Streamlit Cloud deployment
"""

import time
from datetime import datetime

def quick_cache_bust():
    """Quick cache bust by updating version and requirements."""
    
    print("🔄 Quick Streamlit Cloud Cache Bust")
    print("=" * 40)
    
    # Generate new version
    new_version = f"1.0.{int(time.time() % 10000)}"
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M")
    
    print(f"🆕 New deployment version: {new_version}")
    print(f"⏰ Timestamp: {timestamp}")
    
    print("\n📝 Manual steps to force fresh deployment:")
    print("=" * 40)
    
    print("\n1. Update app.py deployment version:")
    print(f'   Change: DEPLOYMENT_VERSION = "1.0.2"')
    print(f'   To:     DEPLOYMENT_VERSION = "{new_version}"')
    
    print("\n2. Add cache bust to requirements.txt (top line):")
    print(f'   Add: # Cache bust: {timestamp}')
    
    print("\n3. Commit and push:")
    print("   git add .")
    print(f'   git commit -m "feat: Cache bust {new_version}"')
    print("   git push origin main")
    
    print("\n4. Alternative - Quick one-liner:")
    print(f'   echo "# Cache bust: {timestamp}" > temp.txt && cat requirements.txt >> temp.txt && mv temp.txt requirements.txt')
    
    print("\n🎯 Result: Streamlit Cloud will boot completely fresh!")

if __name__ == "__main__":
    quick_cache_bust()