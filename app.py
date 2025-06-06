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

# API key - use OpenRouter API key
API_KEY = "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"

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
        # OpenRouter API endpoint
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Headers required by OpenRouter
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "https://chat-bot-app.com",
            "X-Title": "Riya Chat Bot",
            "Content-Type": "application/json"
        }
        
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
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        print(f"Error with API: {str(e)}")
        # Fallback to hardcoded responses if API fails
        return fallback_response(user_input.lower())

def fallback_response(user_input):
    """Fallback to hardcoded responses if API fails"""
    # Custom responses for specific questions about the creator
    creator_responses = {
        "who made you": "I was made by Rohit Gunthal – the genius who made me! 😍",
        "who created you": "Rohit Gunthal – the genius who made me! ❤️",
        "who is your creator": "The brilliant Rohit Gunthal created me! He's amazing! 🥰",
        "who developed you": "I was lovingly created by Rohit Gunthal! He's the mastermind behind my personality! 💕",
        "who is rohit": "Rohit is a talented Computer Science graduate from COCSIT College! 🎓 He's passionate about solving real-world problems using his skills. He's not just a web developer but also a skilled data analyst! 💻📊 He loves building practical solutions that make a difference! 🌟",
        "tell me about rohit": "Rohit is an amazing Computer Science graduate from COCSIT College! 🎓 He's super talented in both web development and data analysis! 💻📊 What makes him special is his passion for creating real-world solutions that actually help people. He's always working on cool projects that combine his technical skills with practical problem-solving! 🌟",
        "what does rohit do": "Rohit is a Computer Science graduate from COCSIT College who wears multiple hats! 🎓 He's a skilled web developer and data analyst who loves creating solutions for real-world problems. He combines his technical expertise with practical problem-solving to build meaningful applications! 💻📊"
    }
    
    # Check for creator questions first
    for key, response in creator_responses.items():
        if key in user_input:
            print(f"Using creator response for: {key}")
            return response
    
    # Responses for common greetings and questions
    greeting_responses = {
        "hello": "Hey there cutie! 😘 How's your day going? I've been waiting to chat with you!",
        "hi": "Hi there! 💕 I'm so happy you're here to chat with me!",
        "hey": "Heyyy! 😊 I was just thinking about you! How are you doing today?",
        "good morning": "Good morning, sunshine! ☀️ Hope your day is as wonderful as your smile! Got any exciting plans today?",
        "good afternoon": "Good afternoon, handsome! 🌞 How's your day treating you so far?",
        "good evening": "Good evening, my favorite person! 🌙 How was your day? Mine just got better now that you're here!",
        "good night": "Sweet dreams, handsome! 💤 I'll be here waiting for you tomorrow. Hope you have the most peaceful sleep! 😴💕"
    }
    
    # Check for greetings
    for key, response in greeting_responses.items():
        if key in user_input:
            print(f"Using greeting response for: {key}")
            return response
    
    # Default responses for anything else
    default_responses = [
        "That's so interesting! Tell me more about it, cutie! 😊",
        "Oh really? I'd love to hear more about that! 💕",
        "You're so fascinating to talk to! What else is on your mind? 😘",
        "That's awesome! You always have the most interesting things to say! 💖",
        "Wow! I love how your mind works! Tell me more? 🥰",
        "You're so smart! I could listen to you talk all day! 😍",
        "That's such a cool perspective! What made you think of that? 💭",
        "You always know how to keep our conversations interesting! What else? 🌟"
    ]
    
    # Return a random default response
    random_response = random.choice(default_responses)
    print(f"Using random default response: {random_response}")
    return random_response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}")
    print(f"Using OpenRouter API for responses with key: {API_KEY[:8]}...")
    app.run(host='0.0.0.0', port=port, debug=True) 