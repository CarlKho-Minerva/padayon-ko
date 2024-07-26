from flask import Flask, request, jsonify, render_template
from google.cloud import speech, texttospeech
import google.generativeai as genai
import os
import io
import tempfile
import base64
import random

app = Flask(__name__)

# Initialize clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Initialize Gemini API
genai.configure(api_key=)
model = genai.GenerativeModel("gemini-pro")


def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,
        language_code="en-US",
    )
    response = speech_client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript


def synthesize_text(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return base64.b64encode(response.audio_content).decode("utf-8")


def gemini_process(user_input, mode):
    prompt = f"""
    Respond to the user's input in a conversational manner, keeping the response around 5 seconds long when spoken.
    Focus on the following mode: {mode}

    1. Debate/Defend: Provide a counterargument or supporting argument.
    2. Narrate/Storytell: Create a brief narrative or story element related to the input.
    3. Explain: Use a metaphor or analogy to explain the concept.
    4. Question Formation/Answering: Generate a relevant question or provide a concise answer.

    User input: {user_input}
    """
    response = model.generate_content(prompt)
    return response.text




@app.route("/")
def index():
    return render_template("index.html")

def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,  # Updated to match the WEBM OPUS header
        language_code="en-US",
    )
    
    try:
        response = speech_client.recognize(config=config, audio=audio)
        
        if not response.results:
            return None  # Return None if no transcription is available
        
        return response.results[0].alternatives[0].transcript
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    mode = request.form.get('mode', 'Debate')  # Default to 'Debate' if no mode is provided
    
    audio_data = audio_file.read()
    
    user_input = transcribe_audio(audio_data)
    
    if user_input is None:
        return jsonify({
            'error': 'Could not transcribe audio. Please try speaking more clearly or for a longer duration.'
        }), 400
    
    ai_response = gemini_process(user_input, mode)
    audio_response = synthesize_text(ai_response)
    
    return jsonify({
        'user_input': user_input,
        'ai_response': ai_response,
        'audio_response': audio_response
    })

@app.route("/get_prompt", methods=["GET"])
def get_prompt():
    prompts = [
        "Discuss a recent technological advancement that excites you.",
        "Share your thoughts on the future of remote work.",
        "What's a book or movie that has greatly influenced your thinking?",
        "Describe an interesting cultural tradition from your background.",
        "If you could solve one global problem, what would it be and why?",
    ]
    return jsonify({"prompt": random.choice(prompts)})


if __name__ == "__main__":
    app.run(debug=True)
