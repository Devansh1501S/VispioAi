#!/usr/bin/env python3
"""
Streamlit Cache Clearing Script
Run this script to clear all Streamlit caches and force fresh deployments.
"""

import streamlit as st
import os
import shutil
import tempfile
import time

def clear_streamlit_cache():
    """Clear all Streamlit cache directories and files."""
    
    print("🧹 Clearing Streamlit cache...")
    
    # Clear Streamlit's internal caches
    try:
        st.cache_data.clear()
        st.cache_resource.clear()
        print("✅ Streamlit internal caches cleared")
    except Exception as e:
        print(f"⚠️ Could not clear internal caches: {e}")
    
    # Clear temporary files
    temp_dirs = [
        tempfile.gettempdir(),
        os.path.expanduser("~/.streamlit"),
        os.path.join(os.getcwd(), ".streamlit")
    ]
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                # Remove cache-related files
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if any(keyword in file.lower() for keyword in ['cache', 'temp', 'tmp']):
                            file_path = os.path.join(root, file)
                            try:
                                os.remove(file_path)
                                print(f"🗑️ Removed: {file_path}")
                            except:
                                pass
                print(f"✅ Cleared cache files in: {temp_dir}")
            except Exception as e:
                print(f"⚠️ Could not clear {temp_dir}: {e}")
    
    # Clear session state
    try:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        print("✅ Session state cleared")
    except Exception as e:
        print(f"⚠️ Could not clear session state: {e}")
    
    print("🎉 Cache clearing complete!")
    print("💡 Restart your Streamlit app for changes to take effect.")

if __name__ == "__main__":
    clear_streamlit_cache() 