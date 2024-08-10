from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from notion_client import Client
from dotenv import load_dotenv
import google.generativeai as genai
from gemini_functions import (
    embed_content,
    find_best_passages,
    generate_scholarship_application,
)
from notion_functions import (
    get_database_id,
    process_foundational_essays,
    process_student_achievements,
)

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Initialize Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GenAI_model = genai.GenerativeModel(model_name="gemini-1.5-pro")
embedding_model = "models/embedding-001"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate_essay", methods=["POST"])
def generate_essay():
    data = request.json
    query = data["query"]
    selected_essays = data["selected_essays"]
    selected_achievements = data["selected_achievements"]

    response = generate_scholarship_application(
        selected_essays, selected_achievements, GenAI_model
    )

    # Split the response into title and content
    essay_parts = response.split("~", 1)
    title = essay_parts[0].strip() if len(essay_parts) > 1 else "Untitled"
    content = essay_parts[1].strip() if len(essay_parts) > 1 else response

    return jsonify({"title": title, "content": content})


@app.route("/query_essays_achievements", methods=["POST"])
def query_essays_achievements():
    data = request.json
    query = data["query"]

    essays_db_id = get_database_id(notion, "Foundational Essays")
    achievements_db_id = get_database_id(notion, "Student Achievements")

    df_essays = process_foundational_essays(notion, essays_db_id)
    df_achievements = process_student_achievements(notion, achievements_db_id)

    top_essays = find_best_passages(query, df_essays)
    top_achievements = find_best_passages(query, df_achievements, top_n=5)

    return jsonify(
        {
            "essays": top_essays[["title", "content"]].to_dict("records"),
            "achievements": top_achievements[["title", "content"]].to_dict("records"),
        }
    )


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)
