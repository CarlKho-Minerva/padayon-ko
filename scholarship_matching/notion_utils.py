from notion_client import Client
from config import NOTION_API_KEY

notion = Client(auth=NOTION_API_KEY)


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
