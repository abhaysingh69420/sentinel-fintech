import google.generativeai as genai

# PASTE YOUR KEY HERE
GOOGLE_API_KEY = "AIzaSyBE3U4YIjLUXGWPwMD__ahwuGFUVHlZlSQ"

genai.configure(api_key=GOOGLE_API_KEY)

print("--- CHECKING AVAILABLE MODELS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found: {m.name}")
except Exception as e:
    print(f"Error: {e}")