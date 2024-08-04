from notion_client import Client
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))


# Function to get database ID by title
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


# Function to create a Facebook post
def create_facebook_post(
    message,
    access_token=os.getenv("FACEBOOK_ACCESS_TOKEN"),
    page_id=os.getenv("FACEBOOK_PAGE_ID"),
):
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "access_token": access_token}
    response = requests.post(url, data=payload)
    return response.json()


# Monitor Notion database for new items with `facebookPostReady?` set to True
def monitor_notion_database(database_id):
    try:
        response = notion.databases.query(database_id=database_id)
        results = response.get("results", [])
        for page in results:
            properties = page.get("properties", {})
            facebook_post_ready = properties.get("facebookPostReady?", {}).get(
                "checkbox", False
            )
            if facebook_post_ready:
                message = (
                    properties.get("Message", {})
                    .get("rich_text", [{}])[0]
                    .get("text", {})
                    .get("content", "")
                )
                if message:
                    facebook_response = create_facebook_post(message)
                    print(f"Facebook response: {facebook_response}")
                else:
                    print("No message found for the Facebook post.")
    except Exception as e:
        print(f"An error occurred while querying the Notion database: {e}")


if __name__ == "__main__":
    database_title = "Scholarship List for Padayun Ko"
    database_id = get_database_id(database_title)
    if database_id:
        monitor_notion_database(database_id)
    else:
        print("Failed to get database ID.")
