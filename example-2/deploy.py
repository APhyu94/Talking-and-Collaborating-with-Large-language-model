#!/usr/bin/env python3
"""
Deployment script for the PDF to Podcast Telegram Bot
Automates the setup and deployment process
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8 or higher.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    return run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    try:
        Path("temp_audio").mkdir(exist_ok=True)
        print("✅ Directories created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("Please run setup_bot.py to configure your API keys")
        return False

def run_tests():
    """Run component tests"""
    return run_command(
        "python test_bot.py",
        "Running component tests"
    )

def main():
    """Main deployment function"""
    print("🚀 PDF to Podcast Bot - Deployment Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check your internet connection.")
        return
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories.")
        return
    
    # Check environment configuration
    if not check_env_file():
        print("\n📝 To configure your bot:")
        print("1. Run: python setup_bot.py")
        print("2. Follow the prompts to enter your API keys")
        print("3. Run this deployment script again")
        return
    
    # Run tests
    if not run_tests():
        print("❌ Component tests failed. Please check the errors above.")
        return
    
    print("\n🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the bot: python telegram_podcast_bot.py")
    print("2. Open your bot in Telegram")
    print("3. Send /start to test the bot")
    print("4. Upload a PDF to generate a podcast!")
    
    print("\n📚 Useful commands:")
    print("- Test components: python test_bot.py")
    print("- Setup API keys: python setup_bot.py")
    print("- View logs: tail -f podcast_bot.log")

if __name__ == "__main__":
    main() 