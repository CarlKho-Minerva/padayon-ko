from flask import Flask, request, jsonify, render_template
from google.cloud import speech, texttospeech
import google.generativeai as genai
import os
import tempfile
import base64
import uuid

app = Flask(__name__)

# Initialize clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Initialize Gemini API
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-pro")

# Store conversations
conversations = {}


def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
    )

    try:
        response = speech_client.recognize(config=config, audio=audio)

        if not response.results:
            return None

        return response.results[0].alternatives[0].transcript
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None


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


def generate_ai_response(conversation_id, user_input, mode):
    if conversation_id not in conversations:
        conversations[conversation_id] = model.start_chat(history=[])

    chat = conversations[conversation_id]

    prompt = f"""
    You are an AI communication assistant. Based on the user's input, your task is to {mode}.
    Respond in a way that encourages further conversation and helps the user improve their communication skills.
    Keep your response concise, around 2-3 sentences.

    User input: {user_input}

    Your response:
    """

    response = chat.send_message(prompt)
    return response.text


@app.route("/process_audio", methods=["POST"])
def process_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    mode = request.form.get("mode", "have a general conversation about")
    conversation_id = request.form.get("conversation_id", str(uuid.uuid4()))

    audio_data = audio_file.read()

    user_input = transcribe_audio(audio_data)

    if user_input is None:
        return (
            jsonify(
                {
                    "error": "Could not transcribe audio. Please try speaking more clearly or for a longer duration."
                }
            ),
            400,
        )

    ai_response = generate_ai_response(conversation_id, user_input, mode)
    audio_response = synthesize_text(ai_response)

    return jsonify(
        {
            "conversation_id": conversation_id,
            "user_input": user_input,
            "ai_response": ai_response,
            "audio_response": audio_response,
        }
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)
