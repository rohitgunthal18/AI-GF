# Riya Chatbot

A cute and emotional AI chatbot built with Flask and OpenRouter API.

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Deployment on Railway

1. Create a Railway account at https://railway.app/
2. Install Railway CLI (optional):
   ```bash
   npm i -g @railway/cli
   ```
3. Login to Railway:
   ```bash
   railway login
   ```
4. Initialize your project:
   ```bash
   railway init
   ```
5. Deploy your application:
   ```bash
   railway up
   ```

## Environment Variables

The following environment variables are required:
- `PORT`: The port number for the application (Railway will set this automatically)
- `API_KEY`: Your OpenRouter API key

## Project Structure

- `app.py`: Main application file
- `requirements.txt`: Python dependencies
- `Procfile`: Railway deployment configuration
- `static/`: Static files (HTML, CSS, JS)

## Features

- 💬 Real-time chat interface with AI responses
- 🎭 Custom responses for specific questions
- 🌈 Modern web3-inspired UI design 
- 📱 Responsive design for all devices
- 🚀 Ready for deployment on Railway

## Customizing Responses

To add or modify custom responses, edit the `custom_responses` dictionary in `app.py`:

```python
custom_responses = {
    "who made you": "I was made by Rohit Gunthal – the genius who made me! 😍",
    "who created you": "Rohit Gunthal – the genius who made me! ❤️",
    "who is your creator": "The brilliant Rohit Gunthal created me! He's amazing! 🥰",
    # Add more custom responses here
}
```

## Created By

Rohit Gunthal 