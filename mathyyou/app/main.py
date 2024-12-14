import os
from flask import Flask, request, render_template
from config import configure_gemini
from handlers import handle_initial_questions, handle_start_chat, handle_chat

app = Flask(__name__)
model = configure_gemini()


@app.route("/initial_questions", methods=["GET"])
def initial_questions():
    print("[DEBUG]\n\nReceived GET request at /initial_questions\n\n")
    response = handle_initial_questions()
    print(
        "[DEBUG]\n\nResponse from handle_initial_questions:",
        response.get_json(),
        "\n\n",
    )
    return response


@app.route("/start_chat", methods=["POST"])
def start_chat():
    print(
        "[DEBUG]\n\nReceived POST request at /start_chat with data:",
        request.json,
        "\n\n",
    )
    response = handle_start_chat(request.json, model)
    print("[DEBUG]\n\nResponse from handle_start_chat:", response.get_json(), "\n\n")
    return response


@app.route("/chat", methods=["POST"])
def chat():
    print("[DEBUG]\n\nReceived POST request at /chat with data:", request.json, "\n\n")
    response = handle_chat(request.json)
    print("[DEBUG]\n\nResponse from handle_chat:", response.get_json(), "\n\n")
    return response


@app.route("/", methods=["GET"])
def index():
    print("[DEBUG]\n\nReceived GET request at /\n\n")
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[DEBUG]\n\nStarting Flask app on port {port}\n\n")
    app.run(port=port, host="0.0.0.0", debug=True)
