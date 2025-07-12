#!/usr/bin/env python3
"""
Test script for the PDF to Podcast Bot
Tests individual components without running the full Telegram bot
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from gtts import gTTS
import PyPDF2
import pdfplumber

# Load environment variables
load_dotenv()

def test_environment():
    """Test if environment variables are set"""
    print("🔧 Testing Environment Configuration...")
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please run setup_bot.py or create a .env file")
        return False
    
    print("✅ Environment variables are configured")
    return True

def test_gemini_api():
    """Test Gemini API connection"""
    print("\n🤖 Testing Gemini API...")
    
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello, this is a test message.")
        
        if response.text:
            print("✅ Gemini API is working correctly")
            return True
        else:
            print("❌ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

def test_pdf_processing():
    """Test PDF text extraction"""
    print("\n📄 Testing PDF Processing...")
    
    # Check if test PDF exists
    test_pdf = Path("DataPrivacy.pdf")
    if not test_pdf.exists():
        print("⚠️  No test PDF found. Skipping PDF processing test.")
        return True
    
    try:
        # Test PyPDF2
        with open(test_pdf, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_pypdf2 = ""
            for page in pdf_reader.pages:
                text_pypdf2 += page.extract_text()
        
        # Test pdfplumber
        with pdfplumber.open(test_pdf) as pdf:
            text_plumber = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_plumber += page_text
        
        if text_pypdf2 or text_plumber:
            print("✅ PDF text extraction is working")
            print(f"   PyPDF2 extracted {len(text_pypdf2)} characters")
            print(f"   pdfplumber extracted {len(text_plumber)} characters")
            return True
        else:
            print("❌ No text extracted from PDF")
            return False
            
    except Exception as e:
        print(f"❌ PDF processing error: {e}")
        return False

def test_tts():
    """Test text-to-speech functionality"""
    print("\n🎵 Testing Text-to-Speech...")
    
    try:
        test_text = "This is a test of the text to speech functionality."
        tts = gTTS(text=test_text, lang='en', slow=False)
        
        # Create temp directory if it doesn't exist
        temp_dir = Path("temp_audio")
        temp_dir.mkdir(exist_ok=True)
        
        # Save test audio
        test_audio_path = temp_dir / "test_audio.mp3"
        tts.save(str(test_audio_path))
        
        if test_audio_path.exists() and test_audio_path.stat().st_size > 0:
            print("✅ Text-to-speech is working correctly")
            # Clean up test file
            test_audio_path.unlink()
            return True
        else:
            print("❌ Text-to-speech failed to generate audio file")
            return False
            
    except Exception as e:
        print(f"❌ Text-to-speech error: {e}")
        return False

def test_script_generation():
    """Test AI script generation"""
    print("\n✍️ Testing Script Generation...")
    
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        test_text = "This is a sample text about artificial intelligence and its applications in modern technology."
        
        prompt = f"""
        Convert this text into a short podcast script (2-3 sentences):
        {test_text}
        """
        
        response = model.generate_content(prompt)
        
        if response.text and len(response.text) > 10:
            print("✅ Script generation is working correctly")
            print(f"   Generated script: {response.text[:100]}...")
            return True
        else:
            print("❌ Script generation returned insufficient content")
            return False
            
    except Exception as e:
        print(f"❌ Script generation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 PDF to Podcast Bot - Component Tests")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_gemini_api,
        test_pdf_processing,
        test_tts,
        test_script_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot should work correctly.")
        print("\nNext steps:")
        print("1. Run: python telegram_podcast_bot.py")
        print("2. Test with your Telegram bot")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Verify your API keys in .env file")
        print("2. Check your internet connection")
        print("3. Ensure all dependencies are installed")

if __name__ == "__main__":
    main() 