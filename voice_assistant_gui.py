from flask import Flask, render_template, jsonify, request
import threading
import queue
import time
import os
import sys
import datetime
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil 
import subprocess
from elevenlabs import text_to_speech, play
from api_key import api_key_data

# Set the API key as environment variable
os.environ["ELEVEN_API_KEY"] = api_key_data

app = Flask(__name__)

# Global variables for voice assistant
voice_queue = queue.Queue()
is_listening = False
current_status = "Ready"
user_name = "Latha"

# Load the AI model and data
try:
    with open("intents.json") as file:
        data = json.load(file)
    model = load_model("chat_model.h5")
    
    # Try to load tokenizer with error handling
    try:
        with open("tokenizer.pkl", "rb") as f:
            tokenizer = pickle.load(f)
    except ModuleNotFoundError:
        print("Warning: Tokenizer was saved with an older version. Creating a simple fallback.")
        from tensorflow.keras.preprocessing.text import Tokenizer
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(["hello", "hi", "how are you", "what is your name"])
    
    with open("label_encoder.pkl", "rb") as encoder_file:
        label_encoder = pickle.load(encoder_file)
except Exception as e:
    print(f"Error loading model: {e}")
    data = {"intents": []}
    model = None
    tokenizer = None
    label_encoder = None

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def engine_talk(query):
    try:
        audio = text_to_speech(
            text=query, 
            voice='Grace',
            model="eleven_monolingual_v1"
        )
        play(audio)
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        speak(query)

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        return f"Good morning {user_name}, it's {day} and the time is {t}"
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        return f"Good afternoon {user_name}, it's {day} and the time is {t}"
    else:
        return f"Good evening {user_name}, it's {day} and the time is {t}"

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
        return "Opening Facebook"
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
        return "Opening WhatsApp"
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
        return "Opening Discord"
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
        return "Opening Instagram"
    else:
        speak("No result found")
        return "No result found"

def schedule():
    day = cal_day().lower()
    speak(f"{user_name} today's schedule is ")
    week={
    "monday": f"{user_name}, from 9:00 to 9:50 you have Algorithms class, from 10:00 to 11:50 you have System Design class, from 12:00 to 2:00 you have a break, and today you have Programming Lab from 2:00 onwards.",
    "tuesday": f"{user_name}, from 9:00 to 9:50 you have Web Development class, from 10:00 to 10:50 you have a break, from 11:00 to 12:50 you have Database Systems class, from 1:00 to 2:00 you have a break, and today you have Open Source Projects lab from 2:00 onwards.",
    "wednesday": f"{user_name}, today you have a full day of classes. From 9:00 to 10:50 you have Machine Learning class, from 11:00 to 11:50 you have Operating Systems class, from 12:00 to 12:50 you have Ethics in Technology class, from 1:00 to 2:00 you have a break, and today you have Software Engineering workshop from 2:00 onwards.",
    "thursday": f"{user_name}, today you have a full day of classes. From 9:00 to 10:50 you have Computer Networks class, from 11:00 to 12:50 you have Cloud Computing class, from 1:00 to 2:00 you have a break, and today you have Cybersecurity lab from 2:00 onwards.",
    "friday": f"{user_name}, today you have a full day of classes. From 9:00 to 9:50 you have Artificial Intelligence class, from 10:00 to 10:50 you have Advanced Programming class, from 11:00 to 12:50 you have UI/UX Design class, from 1:00 to 2:00 you have a break, and today you have Capstone Project work from 2:00 onwards.",
    "saturday": f"{user_name}, today you have a more relaxed day. From 9:00 to 11:50 you have team meetings for your Capstone Project, from 12:00 to 12:50 you have Innovation and Entrepreneurship class, from 1:00 to 2:00 you have a break, and today you have extra time to work on personal development and coding practice from 2:00 onwards.",
    "sunday": f"{user_name}, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work."
    }
    if day in week.keys():
        speak(week[day])
        return week[day]
    return "Schedule not available"

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
        return "Opening Calculator"
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
        return "Opening Notepad"
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')
        return "Opening Paint"

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
        return "Closing Calculator"
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
        return "Closing Notepad"
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')
        return "Closing Paint"

def browsing(query):
    if 'google' in query:
        speak(f"{user_name}, what should i search on google..")
        return "What should I search on Google?"
    # elif 'edge' in query:
    #     speak("opening your microsoft edge")
    #     os.startfile()

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"{user_name} our system have {percentage} percentage battery")

    if percentage>=80:
        speak(f"{user_name} we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak(f"{user_name} we should connect our system to charging point to charge our battery")
    else:
        speak(f"{user_name} we have very low power, please connect to charging otherwise recording should be off...")
    
    return f"CPU: {usage}%, Battery: {percentage}%"

def process_command(query):
    query = query.lower()
    
    if query == "none":
        return "I didn't catch that. Please try again."
    
    elif ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
        return social_media(query)
    
    elif ("university time table" in query) or ("schedule" in query):
        return schedule()
    
    elif ("volume up" in query) or ("increase volume" in query):
        pyautogui.press("volumeup")
        speak("Volume increased")
        return "Volume increased"
    
    elif ("volume down" in query) or ("decrease volume" in query):
        pyautogui.press("volumedown")
        speak("Volume decreased")
        return "Volume decreased"
    
    elif ("volume mute" in query) or ("mute the sound" in query):
        pyautogui.press("volumemute")
        speak("Volume muted")
        return "Volume muted"
    
    elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
        return openApp(query)
    
    elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
        return closeApp(query)
    
    elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
        if model and tokenizer and label_encoder:
            try:
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        response = np.random.choice(i['responses'])
                        speak(response)
                        return response
            except Exception as e:
                return f"AI response error: {str(e)}"
        return "I'm here to help you!"
    
    elif ("open google" in query) or ("open edge" in query):
        return browsing(query)
    
    elif ("system condition" in query) or ("condition of the system" in query):
        speak("checking the system condition")
        return condition()
    
    elif "exit" in query:
        speak("Goodbye! Have a great day!")
        return "Goodbye! Have a great day!"
    
    else:
        return "I'm not sure how to help with that. Try asking me to open an app, check the weather, or ask a question!"

def voice_listener():
    global is_listening, current_status
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)  # Reduced from 0.5
        r.pause_threshold = 0.5  # Reduced from 1.0 - faster response
        r.phrase_threshold = 0.1  # Reduced from 0.3 - more sensitive
        r.sample_rate = 16000  # Reduced from 48000 for faster processing
        r.dynamic_energy_threshold = True
        r.operation_timeout = 3  # Reduced from 5 - faster timeout
        r.non_speaking_duration = 0.3  # Reduced from 0.5 - faster end detection
        r.dynamic_energy_adjustment = 1.5  # Reduced from 2
        r.energy_threshold = 3000  # Reduced from 4000 - more sensitive
        r.phrase_time_limit = 5  # Reduced from 10 - faster processing
        
        while is_listening:
            try:
                current_status = "Listening..."
                audio = r.listen(source, timeout=0.5, phrase_time_limit=5)  # Reduced timeouts
                current_status = "Processing..."
                
                query = r.recognize_google(audio, language='en-in')
                current_status = f"Recognized: {query}"
                
                response = process_command(query)
                voice_queue.put({"query": query, "response": response, "timestamp": time.time()})
                
                current_status = "Ready"
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                current_status = "Ready"
                continue
            except Exception as e:
                current_status = f"Error: {str(e)}"
                continue

@app.route('/')
def index():
    return render_template('index.html', user_name=user_name)

@app.route('/start_listening')
def start_listening():
    global is_listening
    if not is_listening:
        is_listening = True
        threading.Thread(target=voice_listener, daemon=True).start()
        return jsonify({"status": "started", "message": "Voice assistant is now listening!"})
    return jsonify({"status": "already_running", "message": "Already listening!"})

@app.route('/stop_listening')
def stop_listening():
    global is_listening
    is_listening = False
    return jsonify({"status": "stopped", "message": "Voice assistant stopped!"})

@app.route('/get_status')
def get_status():
    global current_status
    return jsonify({"status": current_status})

@app.route('/get_messages')
def get_messages():
    messages = []
    while not voice_queue.empty():
        try:
            messages.append(voice_queue.get_nowait())
        except queue.Empty:
            break
    return jsonify({"messages": messages})

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    query = data.get('query', '')
    response = process_command(query)
    return jsonify({"query": query, "response": response})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("🎉 Voice Assistant GUI created successfully!")
    print("🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🎤 Click 'Start Listening' to begin using your voice assistant!")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 