import os
import textwrap
import numpy as np
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from IPython.display import Markdown

# Import the notion retrieval functions from the previous code
from notion_read_db_toggle_child import (
    get_database_id,
    read_notion_database,
    read_student_achievements_database,
    get_page_content,
    extract_toggle_content,
)

# Load environment variables from .env file
load_dotenv()

# Set up the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
for m in genai.list_models():
    if "embedContent" in m.supported_generation_methods:
        print(m.name)
GenAI_model = genai.GenerativeModel(model_name="gemini-1.5-pro")
model = "models/embedding-001"


def embed_fn(title, text):
    return genai.embed_content(
        model=model, content=text, task_type="retrieval_document", title=title
    )["embedding"]


def find_best_passages(query, dataframe, top_n=3):
    query_embedding = genai.embed_content(
        model=model, content=query, task_type="retrieval_query"
    )["embedding"]
    dot_products = np.dot(np.stack(dataframe["Embeddings"]), query_embedding)
    indices = np.argsort(dot_products)[-top_n:][::-1]
    return dataframe.iloc[indices]


def make_prompt(query, relevant_passages):
    passages_text = " ".join(
        [
            passage.replace("'", "").replace('"', "").replace("\n", " ")
            for passage in relevant_passages
        ]
    )
    prompt = textwrap.dedent(
        """You write essays based on question and passage.
QUESTION: '{query}'
PASSAGES: '{passages_text}'

ANSWER:
"""
    ).format(query=query, passages_text=passages_text)
    return prompt


def main():
    print("Starting main function.")
    query_achievements = "Achievements"  # Replace with your query
    query_essays = "Scholarships"  # Replace with your query

    # Process Foundational Essays
    database_title_essays = "Foundational Essays"
    print(f"Database title: {database_title_essays}")

    database_id_essays = get_database_id(database_title_essays)
    print(f"Retrieved database ID: {database_id_essays}")
    if not database_id_essays:
        print("Failed to retrieve the database ID for essays.")
        return

    database_entries_essays = read_notion_database(database_id_essays)
    print(
        f"Retrieved {len(database_entries_essays) if database_entries_essays else 0} database entries for essays."
    )
    if not database_entries_essays:
        print(
            "No entries found or there was an error retrieving the database for essays."
        )
        return

    essays = []
    for entry in database_entries_essays:
        properties = entry.get("properties", {})
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )

        page_id = entry.get("id")
        print(f"Processing essay entry with title: {title} and page ID: {page_id}")

        page_content = get_page_content(page_id)

        toggle_content = extract_toggle_content(page_content)
        for toggle_title, children in toggle_content.items():
            essay_text = "\n".join(children)
            essays.append({"title": toggle_title, "content": essay_text})
            print(f"Added essay with toggle title: {toggle_title}")
    if not essays:
        print("No toggle content found in essays.")
        return

    df_essays = pd.DataFrame(essays)
    print(f"Created DataFrame with {len(df_essays)} essays.")
    df_essays["Embeddings"] = df_essays.apply(
        lambda row: embed_fn(row["title"], row["content"]), axis=1
    )
    print("Generated embeddings for essays.")

    print(f"Query for essays: {query_essays}")
    top_essays = find_best_passages(query_essays, df_essays)
    print("Found top essays based on query.")
    print("Top 3 Essays:")
    for i, row in top_essays.iterrows():
        print(f"{i + 1}. {row['title']}\n{row['content']}\n")

    selected_indices_essays = input(
        "Select essays by index (comma-separated, e.g., 1,2,3): "
    )

    selected_indices_essays = [int(i) - 1 for i in selected_indices_essays.split(",")]
    selected_essays = [
        top_essays.iloc[idx]["content"] for idx in selected_indices_essays
    ]
    print(f"Selected essays indices: {selected_indices_essays}")

    # Process Student Achievements
    database_title_achievements = "Student Achievements"
    print(f"Database title: {database_title_achievements}")

    database_id_achievements = get_database_id(database_title_achievements)
    print(f"Retrieved database ID: {database_id_achievements}")
    if not database_id_achievements:
        print("Failed to retrieve the database ID for achievements.")
        return

    database_entries_achievements = read_student_achievements_database(
        database_id_achievements
    )
    print(
        f"Retrieved {len(database_entries_achievements) if database_entries_achievements else 0} database entries for achievements."
    )
    if not database_entries_achievements:
        print(
            "No entries found or there was an error retrieving the database for achievements."
        )
        return

    achievements = []
    for entry in database_entries_achievements:
        properties = entry.get("properties", {})
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )
        page_id = entry.get("id")
        print(
            f"Processing achievement entry with title: {title} and page ID: {page_id}"
        )

        page_content = get_page_content(page_id)
        toggle_content = extract_toggle_content(page_content)
        for toggle_title, children in toggle_content.items():
            achievement_text = "\n".join(children)
            achievements.append({"title": toggle_title, "content": achievement_text})
            print(f"Added achievement with toggle title: {toggle_title}")
    if not achievements:
        print("No toggle content found in achievements.")
        return

    df_achievements = pd.DataFrame(achievements)
    print(f"Created DataFrame with {len(df_achievements)} achievements.")
    df_achievements["Embeddings"] = df_achievements.apply(
        lambda row: embed_fn(row["title"], row["content"]), axis=1
    )
    print("Generated embeddings for achievements.")

    query_achievements = "Achievements"  # Replace with your query
    print(f"Query for achievements: {query_achievements}")
    top_achievements = find_best_passages(query_achievements, df_achievements)
    print("Found top achievements based on query.")
    print("Top 5 Achievements:")
    for i, row in top_achievements.iterrows():
        print(f"{i + 1}. {row['title']}\n{row['content']}\n")
    selected_indices_achievements = input(
        "Select achievements by index (comma-separated, e.g., 1,2,3,4,5): "
    )
    selected_indices_achievements = [
        int(i) - 1 for i in selected_indices_achievements.split(",")
    ]
    selected_achievements = [
        top_achievements.iloc[idx]["content"] for idx in selected_indices_achievements
    ]
    print(f"Selected achievements indices: {selected_indices_achievements}")

    # Combine selected essays and achievements into a new essay
    combined_content = selected_essays + selected_achievements
    prompt = make_prompt(query_essays, combined_content)
    print("Generated Prompt:\n", prompt)
    response = GenAI_model.generate_content(prompt)
    print("Generated Response:\n", response.text)


if __name__ == "__main__":
    main()
