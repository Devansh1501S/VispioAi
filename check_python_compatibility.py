#!/usr/bin/env python3
"""
Check Python version compatibility for Vispio deployment
"""

import sys
import platform

def check_python_compatibility():
    """Check if current Python version is suitable for deployment."""
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print("🐍 Python Version Compatibility Check")
    print("=" * 50)
    print(f"Current Python: {version_str}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print()
    
    # Define compatibility levels
    if version >= (3, 11) and version < (3, 12):
        status = "🌟 PERFECT"
        recommendation = "Ideal for Streamlit Cloud deployment"
        deploy_ready = True
    elif version >= (3, 10) and version < (3, 11):
        status = "✅ EXCELLENT"
        recommendation = "Great for deployment, very stable"
        deploy_ready = True
    elif version >= (3, 12):
        status = "⚠️ NEWER"
        recommendation = "Works but may have compatibility issues"
        deploy_ready = True
    elif version >= (3, 9) and version < (3, 10):
        status = "✅ GOOD"
        recommendation = "Acceptable, but consider upgrading"
        deploy_ready = True
    else:
        status = "❌ OUTDATED"
        recommendation = "Upgrade required for best compatibility"
        deploy_ready = False
    
    print(f"Status: {status}")
    print(f"Recommendation: {recommendation}")
    print()
    
    # Check specific package compatibility
    print("📦 Package Compatibility:")
    
    try:
        import streamlit
        st_version = streamlit.__version__
        print(f"✅ Streamlit {st_version} - Compatible")
    except ImportError:
        print("❌ Streamlit - Not installed")
    
    try:
        import google.generativeai
        genai_version = google.generativeai.__version__
        print(f"✅ Google GenerativeAI {genai_version} - Compatible")
    except ImportError:
        print("❌ Google GenerativeAI - Not installed")
    
    try:
        import pygame
        pygame_version = pygame.version.ver
        print(f"✅ Pygame {pygame_version} - Compatible")
    except ImportError:
        print("❌ Pygame - Not installed")
    
    print()
    
    # Deployment recommendations
    print("🚀 Deployment Recommendations:")
    
    if version >= (3, 11) and version < (3, 12):
        print("✅ Perfect for Streamlit Cloud")
        print("✅ Use current version in runtime.txt")
        runtime_version = version_str
    elif version >= (3, 12):
        print("⚠️ Consider using Python 3.11.9 for deployment")
        print("⚠️ Your current version may work but 3.11 is more stable")
        runtime_version = "3.11.9"
    else:
        print("✅ Good for deployment")
        runtime_version = version_str
    
    print(f"\n📝 Recommended runtime.txt content:")
    print(f"python-{runtime_version}")
    
    return deploy_ready, runtime_version

if __name__ == "__main__":
    ready, runtime_ver = check_python_compatibility()
    
    if ready:
        print(f"\n🎉 Ready for deployment with Python {runtime_ver}!")
    else:
        print(f"\n⚠️ Consider upgrading Python for better compatibility")