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
    database_title = "Foundational Essays"
    print(f"Database title: {database_title}")

    database_id = get_database_id(database_title)
    print(f"Retrieved database ID: {database_id}")
    if not database_id:
        print("Failed to retrieve the database ID.")
        return

    database_entries = read_notion_database(database_id)
    print(
        f"Retrieved {len(database_entries) if database_entries else 0} database entries."
    )
    if not database_entries:
        print("No entries found or there was an error retrieving the database.")
        return

    essays = []
    for entry in database_entries:
        properties = entry.get("properties", {})
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )
        page_id = entry.get("id")
        print(f"Processing entry with title: {title} and page ID: {page_id}")

        page_content = get_page_content(page_id)
        toggle_content = extract_toggle_content(page_content)

        for toggle_title, children in toggle_content.items():
            essay_text = "\n".join(children)
            essays.append({"title": toggle_title, "content": essay_text})
            print(f"Added essay with toggle title: {toggle_title}")

    if not essays:
        print("No toggle content found.")
        return

    df = pd.DataFrame(essays)
    print(f"Created DataFrame with {len(df)} essays.")

    df["Embeddings"] = df.apply(
        lambda row: embed_fn(row["title"], row["content"]), axis=1
    )
    print("Generated embeddings for essays.")

    query = "Make a sample essay no matter the input. Just write!"  # Replace with your query
    print(f"Query: {query}")

    top_essays = find_best_passages(query, df)
    print("Found top essays based on query.")

    print("Top 3 Essays:")
    for i, row in top_essays.iterrows():
        print(f"{i + 1}. {row['title']}\n{row['content']}\n")

    # Select multiple essays out of the top 3
    selected_indices = input("Select essays by index (comma-separated, e.g., 1,2,3): ")
    selected_indices = [int(i) - 1 for i in selected_indices.split(",")]
    selected_essays = [top_essays.iloc[idx]["content"] for idx in selected_indices]
    print(f"Selected essays indices: {selected_indices}")

    prompt = make_prompt(query, selected_essays)
    print("Generated Prompt:\n", prompt)

    response = GenAI_model.generate_content(prompt)
    print("Generated Response:\n", response.text)


if __name__ == "__main__":
    main()
