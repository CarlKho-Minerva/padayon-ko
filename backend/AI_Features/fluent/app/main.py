from flask import Flask, request, jsonify, render_template
import os
from speech_utils import transcribe_audio, synthesize_text
from gemini_utils import generate_ai_response, generate_feedback
import uuid
import tempfile

app = Flask(__name__)
DEBUG_MODE = True


def debug_print(message):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(message)


@app.route("/process_audio", methods=["POST"])
def process_audio():
    debug_print("Received request to /process_audio")
    if "audio" not in request.files:
        debug_print("No audio file provided in request")
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    mode = request.form.get("mode", "have a general conversation about")
    conversation_id = request.form.get("conversation_id", str(uuid.uuid4()))
    debug_print(
        f"Processing audio file with conversation_id: {conversation_id} and mode: {mode}"
    )

    try:
        # Save the audio file temporarily
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name

        user_input = transcribe_audio(temp_audio_path)
        debug_print(f"Transcribed audio to text: {user_input}")

        # Remove the temporary audio file
        os.remove(temp_audio_path)

        if user_input is None:
            debug_print("Could not transcribe audio")
            return (
                jsonify(
                    {
                        "error": "Could not transcribe audio. Please try speaking more clearly or for a longer duration."
                    }
                ),
                400,
            )

        ai_response = generate_ai_response(conversation_id, user_input, mode)
        debug_print(f"Generated AI response: {ai_response}")

        audio_response = synthesize_text(ai_response)
        debug_print("Synthesized text to audio")

        if audio_response is None:
            return jsonify({"error": "Could not synthesize audio response"}), 500

        return jsonify(
            {
                "conversation_id": conversation_id,
                "user_input": user_input,
                "ai_response": ai_response,
                "audio_response": audio_response,
            }
        )
    except Exception as e:
        debug_print(f"Error processing audio: {str(e)}")
        return jsonify({"error": f"Error processing audio: {str(e)}"}), 500


@app.route("/get_feedback", methods=["POST"])
def get_feedback():
    debug_print("Received request to /get_feedback")
    mode = request.form.get("mode", "general conversation")
    conversation_id = request.form.get("conversation_id")
    debug_print(
        f"Generating feedback for conversation_id: {conversation_id} and mode: {mode}"
    )
    feedback = generate_feedback(conversation_id, mode)
    debug_print(f"Generated feedback: {feedback}")
    return jsonify({"feedback": feedback})


@app.route("/", methods=["GET"])
def index():
    debug_print("Rendering index.html")
    return render_template("index.html")


if __name__ == "__main__":
    debug_print("Starting Flask app")
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)
