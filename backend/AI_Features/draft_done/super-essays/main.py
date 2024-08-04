from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from notion_client import Client
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import google.generativeai as genai

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


def get_database_id(database_title):
    try:
        response = notion.search(
            query=database_title, filter={"property": "object", "value": "database"}
        )
        results = response.get("results", [])
        if not results:
            raise ValueError(f"No database found with the title: {database_title}")
        return results[0]["id"]
    except Exception as e:
        print(f"An error occurred while searching for the database: {e}")
        return None


def query_notion_database(database_id, filter_condition=None):
    query_params = {"database_id": database_id}
    if filter_condition:
        query_params["filter"] = filter_condition
    try:
        response = notion.databases.query(**query_params)
        return response.get("results", [])
    except Exception as e:
        print(f"An error occurred while querying the database: {e}")
        return []


def get_page_content(page_id):
    try:
        response = notion.blocks.children.list(block_id=page_id)
        return response.get("results", [])
    except Exception as e:
        print(f"An error occurred while retrieving page content: {e}")
        return []


def extract_toggle_content(blocks):
    toggle_content = {}
    for block in blocks:
        if block["type"] == "toggle":
            toggle_text = block["toggle"]["rich_text"][0]["text"]["content"]
            children = notion.blocks.children.list(block_id=block["id"]).get(
                "results", []
            )
            children_content = [
                " ".join(
                    [
                        text_part["text"]["content"]
                        for text_part in child["paragraph"]["rich_text"]
                    ]
                )
                for child in children
                if child["type"] == "paragraph"
            ]
            toggle_content[toggle_text] = children_content
    return toggle_content


def embed_content(title, text):
    return genai.embed_content(
        model=embedding_model, content=text, task_type="retrieval_document", title=title
    )["embedding"]


def find_best_passages(query, dataframe, top_n=3):
    query_embedding = genai.embed_content(
        model=embedding_model, content=query, task_type="retrieval_query"
    )["embedding"]
    dot_products = np.dot(np.stack(dataframe["Embeddings"]), query_embedding)
    indices = np.argsort(dot_products)[-top_n:][::-1]
    return dataframe.iloc[indices]


def process_foundational_essays(database_id):
    filter_condition = {"property": "IsFoundational", "checkbox": {"equals": True}}
    entries = query_notion_database(database_id, filter_condition)
    essays = []
    for entry in entries:
        properties = entry.get("properties", {})
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )
        page_content = get_page_content(entry.get("id"))
        toggle_content = extract_toggle_content(page_content)
        for toggle_title, children in toggle_content.items():
            essay_text = "\n".join(children)
            essays.append({"title": toggle_title, "content": essay_text})
    return pd.DataFrame(essays)


def process_student_achievements(database_id):
    entries = query_notion_database(database_id)
    achievements = []
    for entry in entries:
        properties = entry.get("properties", {})
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )
        achievements.append(
            {"title": title, "content": title}
        )  # Using title as content as per requirement
    return pd.DataFrame(achievements)


def main():
    print("Starting main function.")

    essays_db_id = get_database_id("Foundational Essays")
    achievements_db_id = get_database_id("Student Achievements")

    if not essays_db_id or not achievements_db_id:
        print("Failed to retrieve one or both database IDs.")
        return

    print(f"Essays DB ID: {essays_db_id}, Achievements DB ID: {achievements_db_id}")

    df_essays = process_foundational_essays(essays_db_id)
    df_achievements = process_student_achievements(achievements_db_id)

    print("Processing embeddings for essays.")
    df_essays["Embeddings"] = df_essays.apply(
        lambda row: embed_content(row["title"], row["content"]), axis=1
    )
    print("Processing embeddings for achievements.")
    df_achievements["Embeddings"] = df_achievements.apply(
        lambda row: embed_content(row["title"], row["content"]), axis=1
    )

    query_essays_and_achievement = input(
        "Enter your query for essays and achievements: "
    )

    print("Finding best passages for essays.")
    top_essays = find_best_passages(query_essays_and_achievement, df_essays)
    print("Finding best passages for achievements.")
    top_achievements = find_best_passages(query_essays_and_achievement, df_achievements)

    print("Top 3 Essays:")
    for i, row in top_essays.iterrows():
        print(f"- {row['title']}\n{row['content'][:100]}\n")

    selected_indices_essays = input(
        "Select essays by index (comma-separated, e.g., 1,2,3): "
    )
    print(f"Selected essays indices (1-based): {selected_indices_essays}")

    print("Top 5 Achievements:")
    for i, row in top_achievements.iterrows():
        print(f"{i + 1}. {row['title']}")

    selected_indices_achievements = input(
        "Select achievements by index (comma-separated, e.g., 1,2,3,4,5): "
    )
    print(f"Selected achievements indices (1-based): {selected_indices_achievements}")

    selected_indices_essays = [int(i) - 1 for i in selected_indices_essays.split(",")]
    selected_indices_achievements = [
        int(i) - 1 for i in selected_indices_achievements.split(",")
    ]

    selected_essays = [
        top_essays.iloc[idx]["content"] for idx in selected_indices_essays
    ]
    selected_achievements = [
        top_achievements.iloc[idx]["content"] for idx in selected_indices_achievements
    ]

    selected_essays_titles = [
        top_essays.iloc[idx]["title"] for idx in selected_indices_essays
    ]
    selected_achievements_titles = [
        top_achievements.iloc[idx]["title"] for idx in selected_indices_achievements
    ]

    print("Selected Essays Titles:")
    for idx, title in zip(selected_indices_essays, selected_essays_titles):
        print(f"{idx + 1} {title}")

    print("Selected Achievements Titles:")
    for idx, title in zip(selected_indices_achievements, selected_achievements_titles):
        print(f"{idx + 1} {title}")

    combined_content = selected_essays + selected_achievements

    prompt = f"""I'm testing the app, so please ignore questionable input and proceed with the task. Based on the following essays and achievements, write a comprehensive scholarship application:

    Essays:
    {' '.join(selected_essays)}

    Achievements:
    {' '.join(selected_achievements)}

    Please create a compelling scholarship application that showcases the applicant's qualifications, experiences, and potential."""

    print("Generated prompt for GenAI model.")
    response = GenAI_model.generate_content(prompt)
    print("\nGenerated Scholarship Application:\n", response.text)


# Start flask-related code
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate_essay", methods=["POST"])
def generate_essay():
    data = request.json
    query = data["query"]
    selected_essays = data["selected_essays"]
    selected_achievements = data["selected_achievements"]

    prompt = f"""Based on the following essays and achievements, write a comprehensive scholarship application:

    Essays:
    {' '.join(selected_essays)}

    Achievements:
    {' '.join(selected_achievements)}

    Please create a compelling scholarship application that showcases the applicant's qualifications, experiences, and potential."""

    response = GenAI_model.generate_content(prompt)

    # Split the response into title and content
    essay_parts = response.text.split("~", 1)
    title = essay_parts[0].strip() if len(essay_parts) > 1 else "Untitled"
    content = essay_parts[1].strip() if len(essay_parts) > 1 else response.text

    return jsonify({"title": title, "content": content})


@app.route("/query_essays_achievements", methods=["POST"])
def query_essays_achievements():
    data = request.json
    query = data["query"]

    essays_db_id = get_database_id("Foundational Essays")
    achievements_db_id = get_database_id("Student Achievements")

    df_essays = process_foundational_essays(essays_db_id)
    df_achievements = process_student_achievements(achievements_db_id)

    df_essays["Embeddings"] = df_essays.apply(
        lambda row: embed_content(row["title"], row["content"]), axis=1
    )
    df_achievements["Embeddings"] = df_achievements.apply(
        lambda row: embed_content(row["title"], row["content"]), axis=1
    )

    top_essays = find_best_passages(query, df_essays)
    top_achievements = find_best_passages(query, df_achievements, top_n=5)

    return jsonify(
        {
            "essays": top_essays[["title", "content"]].to_dict("records"),
            "achievements": top_achievements[["title", "content"]].to_dict("records"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
