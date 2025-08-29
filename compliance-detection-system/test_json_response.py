from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

# Test basic JSON response
response = model.generate_content('Please respond with only valid JSON: {"status": "working", "test": true}')

print("Raw response:")
print(response.text)
print("\n" + "="*50)

# Try to parse it
response_text = response.text.strip()

# Handle markdown code blocks
if response_text.startswith('```json') and response_text.endswith('```'):
    response_text = response_text[7:-3].strip()
elif response_text.startswith('```') and response_text.endswith('```'):
    response_text = response_text[3:-3].strip()

print("Cleaned response text:")
print(repr(response_text))
print()

try:
    parsed = json.loads(response_text)
    print("✅ Successfully parsed JSON:")
    print(json.dumps(parsed, indent=2))
except json.JSONDecodeError as e:
    print(f"❌ JSON parsing failed: {e}")
    print("Response may contain markdown or extra text")
