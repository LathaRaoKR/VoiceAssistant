import os
from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Simulated responses for demo purposes
DEMO_RESPONSES = {
    "hello": ["Hello Latha! How can I help you today?", "Hi there! What can I do for you?", "Greetings! How may I assist you?"],
    "time": ["The current time is available on your device.", "I can help you check the time on your system."],
    "schedule": ["Here's your schedule for today: You have a productive day ahead!", "Your schedule is loaded and ready to view."],
    "volume": ["Volume control commands are available.", "I can help you adjust the system volume."],
    "google": ["I can help you search the web.", "Web search functionality is ready."],
    "system": ["System monitoring is available.", "I can check your system status."],
    "default": ["I understand you're interested in AI voice assistants. This is a demonstration of my capabilities.", "That's an interesting question! I'm here to help with various tasks."]
}

@app.route('/')
def index():
    return render_template('index.html', user_name="Latha")

@app.route('/start_listening')
def start_listening():
    return jsonify(status="started")

@app.route('/stop_listening')
def stop_listening():
    return jsonify(status="stopped")

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    query = data.get('query', '').lower()
    
    # Simple keyword matching for demo
    response = "I'm a demo version of the AI assistant. In the full version, I can help with voice commands, system control, and more!"
    
    if any(word in query for word in ['hello', 'hi', 'hey']):
        response = random.choice(DEMO_RESPONSES['hello'])
    elif any(word in query for word in ['time', 'clock']):
        response = random.choice(DEMO_RESPONSES['time'])
    elif any(word in query for word in ['schedule', 'calendar']):
        response = random.choice(DEMO_RESPONSES['schedule'])
    elif any(word in query for word in ['volume', 'sound']):
        response = random.choice(DEMO_RESPONSES['volume'])
    elif any(word in query for word in ['google', 'search']):
        response = random.choice(DEMO_RESPONSES['google'])
    elif any(word in query for word in ['system', 'computer']):
        response = random.choice(DEMO_RESPONSES['system'])
    
    return jsonify(response=response)

@app.route('/get_status')
def get_status():
    return jsonify(status="Ready")

@app.route('/get_messages')
def get_messages():
    return jsonify(messages=[])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 