from flask import request, jsonify, render_template
from notion_database import get_database_id
from notion_helpers import process_foundational_essays, process_student_achievements
from gemini_embedding import find_best_passages
from gemini_text_generation import generate_scholarship_application


def register_routes(app):
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
            selected_essays, selected_achievements, app.config["GenAI_model"]
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

        essays_db_id = get_database_id(app.config["notion"], "Foundational Essays")
        achievements_db_id = get_database_id(
            app.config["notion"], "Student Achievements"
        )

        df_essays = process_foundational_essays(app.config["notion"], essays_db_id)
        df_achievements = process_student_achievements(
            app.config["notion"], achievements_db_id
        )

        top_essays = find_best_passages(query, df_essays)
        top_achievements = find_best_passages(query, df_achievements, top_n=5)

        return jsonify(
            {
                "essays": top_essays[["title", "content"]].to_dict("records"),
                "achievements": top_achievements[["title", "content"]].to_dict(
                    "records"
                ),
            }
        )
