#!/usr/bin/env python3
"""
AI Agent Web UI Launcher

Simple script to launch the Streamlit web interface.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch the Streamlit web UI."""
    print("🚀 Starting AI Agent Web UI...")
    print("📱 The web interface will open in your browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n" + "="*50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Web UI stopped by user")
    except Exception as e:
        print(f"❌ Error starting web UI: {e}")
        print("\n💡 Make sure Streamlit is installed:")
        print("   pip install streamlit")

if __name__ == "__main__":
    main()
