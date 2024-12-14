# Fluent by Padayon Ko

A real-time AI communication practice tool that helps users improve their verbal communication skills through different modes of conversation: debate, storytelling, Q&A, and explanations.

## Features

- **Multiple Practice Modes**
  - 🎭 Debate: Practice structured arguments using SEXI framework
  - 📚 Storytelling: Develop narrative skills with 5C's approach
  - ❓ Q&A: Enhance interviewing skills using OPEN/STAR methods
  - 🎓 Explain: Improve explanation skills with ELI5 technique

- **Real-time Voice Interaction**
  - Voice recording with visual feedback
  - Live transcription
  - AI-generated responses with voice synthesis
  - Individual audio playback controls per message

- **Smart Features**
  - Dynamic conversation prompts
  - Visual recording indicators
  - AI thinking animation
  - Timer with color-coded warnings
  - Detailed conversation feedback

## Tech Stack

- Frontend: HTML, TailwindCSS, JavaScript
- Backend: Flask (Python)
- AI Services:
  - Google Cloud Speech-to-Text
  - Google Cloud Text-to-Speech
  - Google Gemini for AI responses
  - Google Cloud Storage for audio processing

## Deployment Guide

1. **Prerequisites**

   ```bash
   # Install Google Cloud CLI
   # https://cloud.google.com/sdk/docs/install

   # Set up environment variables
   export GEMINI_API_KEY="your_api_key_here"
   ```

2. **Local Development**

   ```bash
   # Install dependencies
   pip install -r requirements.txt

   # Run locally
   python main.py
   ```

3. **Docker Deployment**

   ```bash
   # Build the container
   docker build -t fluent-app .

   # Run locally with Docker
   docker run -p 8080:8080 \
     -e GEMINI_API_KEY="your_api_key_here" \
     fluent-app
   ```

4. **Google Cloud Run Deployment**

   ```bash
   # Login to Google Cloud
   gcloud auth login

   # Set your project
   gcloud config set project YOUR_PROJECT_ID

   # Enable required APIs
   gcloud services enable run.googleapis.com
   gcloud services enable artifactregistry.googleapis.com

   # Deploy to Cloud Run
   gcloud run deploy fluent-app \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars "GEMINI_API_KEY=your_api_key_here"
   ```

## Project Structure

```
fluent/
├── app/
│   ├── templates/
│   │   └── index.html      # Main frontend interface
│   ├── main.py            # Flask application
│   ├── speech_utils.py    # Speech processing utilities
│   ├── gemini_utils.py    # AI conversation handling
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Container configuration
└── README.md
```

## Key Components

1. **Frontend (index.html)**
   - Responsive UI with TailwindCSS
   - Real-time audio recording
   - Dynamic message display
   - Audio playback controls
   - Visual feedback systems

2. **Backend (main.py)**
   - Flask server handling
   - Audio processing endpoints
   - Conversation management
   - Feedback generation

3. **AI Processing (gemini_utils.py)**
   - Conversation context management
   - AI response generation
   - Structured feedback analysis

4. **Speech Processing (speech_utils.py)**
   - Audio transcription
   - Text-to-speech synthesis
   - Google Cloud Storage integration

## Environment Variables

Required environment variables:

- `GEMINI_API_KEY`: Google Gemini API key
- `PORT`: Server port (default: 8080)

## Contributing

Feel free to open issues or submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Credits

Created with 🫶 by Carl Kho (2024)
