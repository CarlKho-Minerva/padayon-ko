import os
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai
from notion_client import Client
import json
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.environ["NOTION_API_KEY"])

# Initialize Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Cache file path
CACHE_FILE = "scholarship_cache.json"
CACHE_EXPIRY_DAYS = 7


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def get_database_id(database_title):
    try:
        print(f"Searching for database with title: {database_title}")
        response = notion.search(
            query=database_title, filter={"property": "object", "value": "database"}
        )
        results = response.get("results", [])
        if not results:
            raise ValueError(f"No database found with the title: {database_title}")
        print(f"Database ID found: {results[0]['id']}")
        return results[0]["id"]
    except Exception as e:
        print(f"An error occurred while searching for the database: {e}")
        return None


def extract_user_profile(database_id):
    try:
        print(f"Extracting user profile from database ID: {database_id}")
        response = notion.databases.query(database_id=database_id)
        user_profile = response["results"][0]["properties"]
        print(f"User profile extracted.")
        return user_profile
    except Exception as e:
        print(f"An error occurred while extracting user profile: {e}")
        return None


def optimize_query(user_profile):
    print(f"Optimizing query for user profile.")
    prompt = f"Optimize this user profile for scholarship matching: {user_profile}"
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    print(f"Optimized query: {response.text}")
    return response.text


def get_scholarship_summaries(database_id):
    try:
        print(f"Getting scholarship summaries from database ID: {database_id}")
        response = notion.databases.query(database_id=database_id)
        summaries = []
        for page in response["results"]:
            title = (
                page["properties"]
                .get("Name", {})
                .get("title", [{}])[0]
                .get("plain_text", "Untitled")
            )
            summary = page["properties"].get("summary", {}).get("rich_text", [])
            page_id = page["id"]
            if summary:
                summaries.append(
                    {
                        "title": title,
                        "summary": summary[0]["plain_text"],
                        "page_id": page_id,
                    }
                )
            else:
                print(
                    f"Excluding scholarship '{title}' due to empty or missing summary."
                )
        print(f"Scholarship summaries: {[s['title'] for s in summaries]}")
        return summaries
    except Exception as e:
        print(f"An error occurred while getting scholarship summaries: {e}")
        return []


def embed_content(title, text, model="models/embedding-001"):
    print(f"Embedding content with title: {title}")
    embedding = genai.embed_content(
        model=model, content=text, task_type="retrieval_document", title=title
    )["embedding"]
    return embedding


def find_best_matches(query, summaries, cache, top_n=3, model="models/embedding-001"):
    print(f"Finding best matches for query.")
    query_embedding = genai.embed_content(
        model=model, content=query, task_type="retrieval_query"
    )["embedding"]

    embedded_summaries = []
    for summary in summaries:
        cache_key = f"{summary['title']}_{summary['summary']}"
        if cache_key in cache and (
            datetime.now() - datetime.fromisoformat(cache[cache_key]["timestamp"])
        ) < timedelta(days=CACHE_EXPIRY_DAYS):
            embedded_summary = cache[cache_key]["embedding"]
        else:
            embedded_summary = embed_content(summary["title"], summary["summary"])
            cache[cache_key] = {
                "embedding": embedded_summary,
                "timestamp": datetime.now().isoformat(),
            }
        embedded_summaries.append(embedded_summary)

    save_cache(cache)

    query_embedding_array = np.array(query_embedding)
    embedded_summaries_array = np.array(embedded_summaries)

    print(f"Query embedding shape: {query_embedding_array.shape}")
    print(f"Embedded summaries shape: {embedded_summaries_array.shape}")

    if query_embedding_array.shape[0] != embedded_summaries_array.shape[1]:
        raise ValueError("Mismatch in dimensions between query and summary embeddings.")

    dot_products = np.dot(embedded_summaries_array, query_embedding_array)
    indices = np.argsort(dot_products)[-top_n:][::-1]
    print(f"Best match indices: {indices}")

    return indices


def get_status_options(database_id):
    print(f"Retrieving status options for database ID: {database_id}")
    database = notion.databases.retrieve(database_id=database_id)
    status_property = database["properties"].get("Status")
    if status_property and status_property["type"] == "status":
        options = status_property["status"]["options"]
        print(f"Status options retrieved.")
        return options
    print("No status options found.")
    return None


def update_scholarship_status(database_id, page_id):
    print(
        f"Updating scholarship status for page ID: {page_id} in database ID: {database_id}"
    )
    status_options = get_status_options(database_id)
    if not status_options:
        print("Error: Could not find Status options in the database.")
        return

    in_progress_option = next(
        (
            option
            for option in status_options
            if option["name"].lower() == "in progress"
        ),
        None,
    )
    if not in_progress_option:
        print("Error: Could not find 'In Progress' status option.")
        return

    try:
        notion.pages.update(
            page_id=page_id,
            properties={"Status": {"status": {"id": in_progress_option["id"]}}},
        )
        print(f"Successfully updated status for page ID: {page_id}")
    except Exception as e:
        print(f"Error updating status for page ID {page_id}: {e}")


def main():
    print("Starting main process")
    user_db_id = get_database_id("Chilipepper DB")
    scholarship_db_id = get_database_id("Scholarship List for Padayun Ko")

    user_profile = extract_user_profile(user_db_id)
    if not user_profile:
        return

    optimized_query = optimize_query(user_profile)

    scholarship_summaries = get_scholarship_summaries(scholarship_db_id)
    if not scholarship_summaries:
        return

    cache = load_cache()
    best_match_indices = find_best_matches(
        optimized_query, scholarship_summaries, cache
    )

    # Update the status of the top 3 matched scholarships
    for index in best_match_indices:
        scholarship = scholarship_summaries[index]
        print(f"Updating status for scholarship: {scholarship['title']}")
        update_scholarship_status(scholarship_db_id, scholarship["page_id"])


if __name__ == "__main__":
    main()
