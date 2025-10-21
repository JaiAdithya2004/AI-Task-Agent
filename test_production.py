#!/usr/bin/env python3
"""
Production Configuration Test

Test the production configuration and dependencies
without requiring Docker to be running.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_production_config():
    """Test production configuration."""
    print("🧪 Testing Production Configuration")
    print("=" * 50)
    
    try:
        # Test config import
        import config
        print("✅ Config module imported successfully")
        
        # Test environment variables
        print(f"   GEMINI_API_KEY: {'Set' if config.GEMINI_API_KEY else 'Not set'}")
        print(f"   GEMINI_MODEL: {config.GEMINI_MODEL}")
        print(f"   GEMINI_TEMPERATURE: {config.GEMINI_TEMPERATURE}")
        print(f"   GEMINI_MAX_TOKENS: {config.GEMINI_MAX_TOKENS}")
        print(f"   LOG_LEVEL: {config.LOG_LEVEL}")
        
        # Test agent import
        from agents.gemini_agent import create_agent, get_agent_info
        print("✅ Gemini agent module imported successfully")
        
        # Test web UI import
        import web_ui
        print("✅ Web UI module imported successfully")
        
        # Test production requirements
        with open("requirements-prod.txt", "r") as f:
            requirements = f.read()
            print(f"✅ Production requirements loaded ({len(requirements.splitlines())} packages)")
        
        print("\n🎉 Production configuration test passed!")
        print("🚀 Ready for Docker deployment!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def show_deployment_structure():
    """Show the deployment file structure."""
    print("\n📁 Production File Structure:")
    print("=" * 50)
    
    essential_files = [
        "Dockerfile",
        ".dockerignore", 
        "render.yaml",
        "requirements-prod.txt",
        "config.py",
        "web_ui.py",
        "run_ui.py",
        "agents/__init__.py",
        "agents/gemini_agent.py",
        "utils/__init__.py",
        "utils/logger.py"
    ]
    
    for file in essential_files:
        path = Path(file)
        if path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (missing)")

def main():
    """Main test function."""
    print("🚀 Autonomous AI Agent - Production Test")
    print("=" * 60)
    
    # Test configuration
    success = test_production_config()
    
    # Show structure
    show_deployment_structure()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Set GEMINI_API_KEY environment variable")
        print("2. Push to GitHub repository")
        print("3. Deploy to Render using render.yaml")
        print("4. Or run locally: docker build -t autonomous-ai-agent .")
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
