#!/usr/bin/env python3
"""
Startup script that tries different approaches to run the server
"""
import subprocess
import sys
import os

def try_install_dependencies():
    """Try to install required dependencies"""
    try:
        # Try to install minimal dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "python-multipart"], check=True)
        print("✓ Basic dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def start_simple_server():
    """Start the simple server"""
    try:
        import uvicorn
        from simple_server import app
        print("🚀 Starting simple floorplan server on http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("✗ Could not start server - missing dependencies")
        return False

def start_full_server():
    """Try to start the full server"""
    try:
        from app.main import app
        import uvicorn
        print("🚀 Starting full floorplan server on http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError as e:
        print(f"✗ Could not start full server: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up Floorplan Recognition API...")
    
    # Try to install dependencies first
    if try_install_dependencies():
        # Try full server first
        if not start_full_server():
            # Fall back to simple server
            start_simple_server()
    else:
        print("❌ Could not install dependencies. Please check your Python environment.")