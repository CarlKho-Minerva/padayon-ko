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

DEBUG_MODE = True


def debug_print(message):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(message)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate_essay", methods=["POST"])
def generate_essay():
    data = request.json
    query = data["query"]
    selected_essays = data["selected_essays"]
    selected_achievements = data["selected_achievements"]

    debug_print(
        f"\n### Starting to generate your scholarship essay for `{query}`. This may take a moment...\n"
    )
    response = generate_scholarship_application(
        query, selected_essays, selected_achievements, GenAI_model
    )

    # Split the response into title and content
    essay_parts = response.split("~", 1)
    title = essay_parts[0].strip() if len(essay_parts) > 1 else ""
    content = essay_parts[1].strip() if len(essay_parts) > 1 else response

    debug_print("\n### Your scholarship application has been generated successfully.\n")
    return jsonify({"title": title, "content": content})


@app.route("/query_essays_achievements", methods=["POST"])
def query_essays_achievements():
    data = request.json
    query = data["query"]

    debug_print(
        "\n### Looking for essays and achievements that match your scholarship prompt...\n"
    )

    debug_print("\n### Fetching the database ID for foundational essays...\n")
    essays_db_id = get_database_id(notion, "Foundational Essays")

    debug_print("\n### Fetching the database ID for student achievements...\n")
    achievements_db_id = get_database_id(notion, "Student Achievements")

    debug_print(
        "\n### Retrieving and analyzing foundational essays from the database...\n"
    )
    df_essays = process_foundational_essays(notion, essays_db_id)

    debug_print(
        "\n### Retrieving and analyzing student achievements from the database...\n"
    )
    df_achievements = process_student_achievements(notion, achievements_db_id)

    debug_print(
        "\n### Finding the best matching essays for your scholarship prompt...\n"
    )
    top_essays = find_best_passages(query, df_essays)

    debug_print(
        "\n### Finding the best matching achievements for your scholarship prompt...\n"
    )
    top_achievements = find_best_passages(query, df_achievements, top_n=5)

    debug_print(
        "\n### Successfully found the best essays and achievements for your scholarship prompt.\n"
    )
    debug_print(
        "\n### Please select the achievements/essays you want to highlight in your essay.\n"
    )
    return jsonify(
        {
            "essays": top_essays[["title", "content"]].to_dict("records"),
            "achievements": top_achievements[["title", "content"]].to_dict("records"),
        }
    )


if __name__ == "__main__":
    debug_print("\n### Starting the application...\n")
    app.run(port=int(os.environ.get("PORT", 8080)), host="0.0.0.0", debug=True)
    debug_print("\n### Application is running. You can now make requests.\n")
