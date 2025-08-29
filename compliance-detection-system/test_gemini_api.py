#!/usr/bin/env python3
"""
Test script to verify Google AI Studio API key setup
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_ai_setup():
    """Test Google AI Studio API configuration"""
    
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ No Google AI Studio API key found")
        print("Please set GOOGLE_API_KEY in your .env file")
        return False
    
    if api_key == "your-google-ai-studio-api-key-here":
        print("❌ Please replace the placeholder API key with your actual key")
        return False
    
    # Test the API key
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Try a simple test
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Say 'API key working' if you can see this.")
        
        print("✅ Google AI Studio API key is working!")
        print(f"📝 Test response: {response.text.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

def show_instructions():
    """Show setup instructions"""
    print("""
🔑 Google AI Studio API Key Setup Instructions:

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key
4. Edit the .env file and replace:
   GOOGLE_API_KEY=your-google-ai-studio-api-key-here
   
   With your actual key:
   GOOGLE_API_KEY=AIzaSyD...your-actual-key-here

5. Save the file and run this test again

💡 Your API key should start with 'AIzaSy'
⚠️  Keep your API key secure and never commit it to version control
""")

if __name__ == "__main__":
    print("🧪 Testing Google AI Studio API Setup...")
    print("=" * 50)
    
    if not test_google_ai_setup():
        show_instructions()
    else:
        print("\n🎉 Setup complete! Your Gemini API is ready to use.")
