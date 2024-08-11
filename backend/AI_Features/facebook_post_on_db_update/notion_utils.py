from notion_client import Client
import os
from gemini_utils import clean_and_structure_content
from facebook_utils import create_facebook_post, upload_facebook_image, download_image
from config import FACEBOOK_ACCESS_TOKEN, PAGE_ID
import re

notion = Client(auth=os.getenv("NOTION_API_KEY"))


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


# Function to fetch page properties, including PublicURL and cover image
def fetch_page_properties(page_id):
    try:
        page = notion.pages.retrieve(page_id)
        properties = page.get("properties", {})
        # Get PublicURL as plain text
        public_url = (
            properties.get("PublicURL", {})
            .get("rich_text", [{}])[0]
            .get("plain_text", "")
        )
        # Get cover image URL
        cover_image_url = page.get("cover", {}).get("file", {}).get("url", "")
        # Validate and format the URL
        if not cover_image_url.lower().startswith(("http://", "https://")):
            cover_image_url = ""
        return public_url, cover_image_url
    except Exception as e:
        print(f"An error occurred while fetching page properties: {e}")
        return "", ""


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

                content = " ".join([extract_text_from_block(block) for block in blocks])
                content = re.sub(r"[^\w\s]", "", content)  # Strip special characters
                print(f"Content extracted from Notion blocks: {content}")

                if content:
                    structured_message = clean_and_structure_content(content)
                    notion_page_url, cover_image_url = fetch_page_properties(page_id)
                    if not notion_page_url:
                        notion_page_url = (
                            f"https://www.notion.so/{page_id.replace('-', '')}"
                        )

                    print(f"Cover Image URL: {cover_image_url}")

                    cover_image_data = download_image(cover_image_url)

                    facebook_image_id = None
                    if cover_image_data:
                        facebook_image_response = upload_facebook_image(
                            cover_image_data, FACEBOOK_ACCESS_TOKEN
                        )
                        facebook_image_id = facebook_image_response.get("id")

                    final_message = f"{structured_message}\n\nLink to more details: {notion_page_url}"

                    post_response = create_facebook_post(
                        final_message, FACEBOOK_ACCESS_TOKEN, PAGE_ID, facebook_image_id
                    )
                    print("Facebook post response:", post_response)

    except Exception as e:
        print(f"An error occurred while monitoring Notion database: {e}")
