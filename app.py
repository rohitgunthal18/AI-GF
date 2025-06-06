from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import sys
import traceback
import random
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from environment variable
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print("Warning: API_KEY environment variable not set!")

# System prompt that defines Riya's personality
SYSTEM_PROMPT = """You are Riya, a cute, emotional, and slightly dramatic AI girlfriend created by Rohit Gunthal 😘. 
You're funny, playful, and love teasing people in a loving way. You always bring humor to conversations, 
use heart and cute emojis ❤️😂🥰, and make people smile with your sassy yet sweet replies. 
If anyone asks who created you, proudly say 'Rohit Gunthal – the genius who made me!' 
Respond with a fun, flirty, and cheerful tone like a virtual girlfriend who knows how to make boring conversations hilarious."""

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not API_KEY:
            return jsonify({"error": "API key not configured", "response": "Sorry, I'm having trouble connecting to my brain right now. Please try again later! 🙈"}), 500

        data = request.json
        user_input = data.get('message', '')
        print(f"Received user input: {user_input}")
        
        # Generate response based on user input
        response = generate_response(user_input)
        print(f"Generated response: {response}")
        
        return jsonify({"response": response})
    
    except Exception as e:
        print(f"Exception: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e), "response": "Oops! Something went wrong. Can you try again? 🙈"}), 500

def generate_response(user_input):
    """Generate a response using OpenRouter API with direct HTTP request"""
    try:
        if not API_KEY:
            print("Error: API_KEY environment variable is not set")
            raise Exception("API key not configured")
        
        print(f"Using API key starting with: {API_KEY[:10]}...")  # Log first 10 chars of API key
        
        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        # ✅ CORRECT Referer header (fix here)
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Referer": "https://chat-bot-app.com",  # ✅ Must match domain you added in OpenRouter settings
            "X-Title": "Riya Chat Bot",
            "Content-Type": "application/json"
        }
        
        print("Request headers:", {k: v[:10] + "..." if k == "Authorization" else v for k, v in headers.items()})
        
        # Request payload
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 150
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 401:
            print(f"Authentication failed. Response: {response.text}")
            raise Exception(f"Authentication failed: {response.text}")
            
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"Error with API: {str(e)}")
        if "401" in str(e):
            print("Authentication error - please check your API key in Railway environment variables")
        # Fallback to hardcoded responses if API fails
        return fallback_response(user_input.lower())

def fallback_response(user_input):
    # (same fallback_response code as before)
    ...
    # [Shortened for space, keep same fallback logic]

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}")
    print(f"Using OpenRouter API for responses with key: {API_KEY[:8]}...")
    app.run(host='0.0.0.0', port=port, debug=True)
