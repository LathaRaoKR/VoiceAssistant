# Latha's AI Voice Assistant

A beautiful, modern AI-powered voice assistant with a stunning web interface. Built with Flask, TensorFlow, and advanced web technologies.

## 🌟 Features

- **Advanced Voice Recognition** - Powered by speech recognition and NLP
- **Beautiful Web Interface** - Modern glassmorphism design with animations
- **Real-time Communication** - Instant voice and text interaction
- **System Integration** - Control volume, apps, and system functions
- **Smart Scheduling** - Personalized daily schedule management
- **Web Search** - Google search integration
- **Responsive Design** - Works perfectly on all devices

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python voice_assistant_gui.py

# Open your browser to http://localhost:5000
```

### Demo Version (Deployment Ready)
```bash
# Run the demo version
python app.py

# Open your browser to http://localhost:5000
```

## 🛠️ Technologies Used

- **Backend**: Flask, Python
- **AI/ML**: TensorFlow, scikit-learn, speech recognition
- **Frontend**: HTML5, CSS3, JavaScript
- **Design**: Modern glassmorphism, responsive design
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## 📦 Deployment Options

### 1. Heroku (Recommended for Demo)

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Open your app**
   ```bash
   heroku open
   ```

### 2. Railway

1. **Connect your GitHub repository**
2. **Railway will automatically detect and deploy**
3. **Get your live URL instantly**

### 3. Render

1. **Connect your GitHub repository**
2. **Select Python environment**
3. **Set build command**: `pip install -r requirements.txt`
4. **Set start command**: `python app.py`
5. **Deploy automatically**

### 4. Python Anywhere

1. **Upload your files**
2. **Install requirements**: `pip install -r requirements.txt`
3. **Configure WSGI file**
4. **Set up your domain**

## 📁 Project Structure

```
Voiceassistant/
├── app.py                 # Demo version for deployment
├── voice_assistant_gui.py # Full version with voice features
├── main.py               # Core voice assistant logic
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment config
├── runtime.txt          # Python version
├── templates/
│   └── index.html       # Beautiful web interface
├── api_key.py           # API keys (not included in repo)
├── chat_model.h5        # AI model
├── tokenizer.pkl        # NLP tokenizer
├── label_encoder.pkl    # Label encoder
└── intents.json         # Training data
```

## 🎯 Resume Highlights

This project demonstrates:

- **Full-Stack Development** - Flask backend + modern frontend
- **AI/ML Integration** - TensorFlow, NLP, speech recognition
- **Modern Web Technologies** - Responsive design, animations
- **API Integration** - ElevenLabs, system APIs
- **Professional UI/UX** - Glassmorphism, micro-interactions
- **Deployment Skills** - Cloud platform deployment
- **Real-time Features** - WebSocket-like communication

## 🔧 Configuration

### Environment Variables
- `ELEVEN_API_KEY`: Your ElevenLabs API key
- `PORT`: Server port (set by deployment platform)

### Local Development
The full version (`voice_assistant_gui.py`) includes:
- Voice recognition
- System control
- Real AI responses

### Deployment
The demo version (`app.py`) includes:
- Beautiful interface
- Simulated AI responses
- No voice dependencies

## 🌐 Live Demo

Visit the deployed version to see the beautiful interface in action!

## 📞 Contact

For questions or collaboration opportunities, feel free to reach out!

---

**Built with ❤️ by Latha** 