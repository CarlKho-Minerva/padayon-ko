import os
from flask import Flask, request, render_template
from config import configure_gemini
from handlers import handle_initial_questions, handle_start_chat, handle_chat

app = Flask(__name__)
model = configure_gemini()


@app.route("/initial_questions", methods=["GET"])
def initial_questions():
    return handle_initial_questions()


@app.route("/start_chat", methods=["POST"])
def start_chat():
    return handle_start_chat(request.json, model)


@app.route("/chat", methods=["POST"])
def chat():
    return handle_chat(request.json)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(port=port, host="0.0.0.0", debug=False)
