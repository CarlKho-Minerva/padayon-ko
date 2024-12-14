from flask import Flask, request, jsonify, render_template, Response
import json
import os
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


@app.route("/process-stream")
def process_stream():
    essay_type = request.args.get("essay_type")
    user_input = request.args.get("essay_content")
    needs_translation = request.args.get("needs_translation") == "true"

    def generate():
        def send_progress(step):
            return f"data: {json.dumps({'step': step})}\n\n"

        yield send_progress("cleaning")
        # Cleaning step processing
        yield send_progress("processing")
        # Processing step
        yield send_progress("refining")
        # Refining step
        yield send_progress("formatting")
        # Final formatting

        final_essay = process_essay(essay_type, user_input, needs_translation)
        yield f"data: {json.dumps({'final_essay': final_essay})}\n\n"

    return Response(generate(), mimetype="text/event-stream")