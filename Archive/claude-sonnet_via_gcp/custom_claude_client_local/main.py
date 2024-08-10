import os
from flask import Flask, request, jsonify, render_template
from anthropic import AnthropicVertex
from google.cloud import speech

app = Flask(__name__)

# Initialize AnthropicVertex client
LOCATION = "us-east5"  # e.g., "us-central1"
PROJECT_ID = "padayon-ko-gemini"
MODEL = "claude-3-5-sonnet@20240620"
anthropic_client = AnthropicVertex(region=LOCATION, project_id=PROJECT_ID)
ENDPOINT = f"https://{LOCATION}-aiplatform.googleapis.com"

# # Initialize Google Speech-to-Text client
speech_client = speech.SpeechClient()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data["messages"]

    response = anthropic_client.messages.create(
        model=MODEL, max_tokens=1024, messages=messages
    )

    return jsonify({"response": response.content[0].text})


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    audio_file = request.files["audio"]

    audio = speech.RecognitionAudio(content=audio_file.read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)

    transcript = (
        response.results[0].alternatives[0].transcript if response.results else ""
    )

    return jsonify({"transcript": transcript})


if __name__ == "__main__":
    app.run(debug=True)
