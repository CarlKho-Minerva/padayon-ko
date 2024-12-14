from flask import Flask, request, jsonify, render_template
from essay_processor import process_essay

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    essay_type = data["essay_type"]
    user_input = data["essay_content"]
    needs_translation = data["needs_translation"]

    final_essay = process_essay(essay_type, user_input, needs_translation)

    return jsonify({"processed_essay": final_essay})
