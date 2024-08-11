from flask import Flask, request, jsonify, render_template
import os
from speech_utils import transcribe_audio, synthesize_text
from gemini_utils import generate_ai_response
import uuid

app = Flask(__name__)


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
