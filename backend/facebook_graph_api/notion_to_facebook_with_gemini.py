from notion_client import Client
import requests
import os
import re

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


# Function to extract content from various block types
def extract_text_from_block(block):
    block_type = block.get("type")
    if block_type == "paragraph":
        return " ".join(
            [
                text.get("plain_text", "")
                for text in block.get("paragraph", {}).get("rich_text", [])
            ]
        )
    elif block_type == "heading_1":
        return " ".join(
            [
                text.get("plain_text", "")
                for text in block.get("heading_1", {}).get("rich_text", [])
            ]
        )
    elif block_type == "heading_2":
        return " ".join(
            [
                text.get("plain_text", "")
                for text in block.get("heading_2", {}).get("rich_text", [])
            ]
        )
    elif block_type == "heading_3":
        return " ".join(
            [
                text.get("plain_text", "")
                for text in block.get("heading_3", {}).get("rich_text", [])
            ]
        )
    elif block_type == "bulleted_list_item":
        return " ".join(
            [
                text.get("plain_text", "")
                for text in block.get("bulleted_list_item", {}).get("rich_text", [])
            ]
        )
    elif block_type == "numbered_list_item":
        return " ".join(
            [
                text.get("plain_text", "")
                for text in block.get("numbered_list_item", {}).get("rich_text", [])
            ]
        )
    elif block_type == "to_do":
        # Handling checkboxes in to-do list
        text = " ".join(
            [
                text.get("plain_text", "")
                for text in block.get("to_do", {}).get("rich_text", [])
            ]
        )
        checked = block.get("to_do", {}).get("checked", False)
        return f"- [x] {text}" if checked else f"- [ ] {text}"
    return ""


# Function to fetch all child blocks of a database item
def fetch_all_child_blocks(page_id):
    blocks = []
    try:
        block_children = notion.blocks.children.list(block_id=page_id)
        while block_children:
            blocks.extend(block_children.get("results", []))
            if block_children.get("next_cursor"):
                block_children = notion.blocks.children.list(
                    block_id=page_id, start_cursor=block_children.get("next_cursor")
                )
            else:
                break
    except Exception as e:
        print(f"An error occurred while fetching child blocks: {e}")
    return blocks


# Function to create a Facebook post
def create_facebook_post(message, access_token, page_id):
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
                page_id = page.get("id")
                print(f"Fetching blocks for page ID: {page_id}")
                blocks = fetch_all_child_blocks(page_id)

                # Debug: Print each block's data
                # for block in blocks:
                # print(f"Block data: {block}")

                content = " ".join([extract_text_from_block(block) for block in blocks])
                content = re.sub(r"[^\w\s]", "", content)  # Strip special characters
                print(f"Content extracted from Notion blocks: {content}")

                if content:
                    # Replace with actual access token and page ID
                    access_token = "EAALn51qddPIBO3vVPEbS9sB1bdLPMX2lkmBj0ZCNz7bEzlpstZAKnXPGeSzRYWUffXlGEzn5IZC75TLi3mWq233jZBTmoXVBtqIQ2qoCLDRMaoYP5XpyyY6y40ERZAsZAHJZCV78d2ZBke9YdFK1sVHH6FdJCsAWACQQH1essFTHFnAMoN5fWHIdml2B65ZCyAptCFSkqwDxZCbPZBNmphgT64EzvZByw0FZBGojBkMGc1Wzw"
                    page_id = "394193433777965"
                    facebook_response = create_facebook_post(
                        content, access_token, page_id
                    )
                    print(f"Facebook response: {facebook_response}")
                else:
                    print("No content found for the Facebook post.")
    except Exception as e:
        print(f"An error occurred while querying the Notion database: {e}")


if __name__ == "__main__":
    database_title = "Scholarship List for Padayun Ko"
    database_id = get_database_id(database_title)
    if database_id:
        monitor_notion_database(database_id)
    else:
        print("Failed to get database ID.")
