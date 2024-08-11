from notion_client import Client
import os
from prompt_fb_caption import clean_and_structure_content
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


def extract_page_properties(page_id):
    try:
        page = notion.pages.retrieve(page_id)
        properties = page.get("properties", {})

        extracted_properties = {
            "For which major or course?": [],
            "Who can apply?": "",
            "What do I get?": [],
            "Until when can I apply?": "",
            "PublicURL": "",
            "cover_image_url": "",
        }

        for prop_name, prop_data in properties.items():
            if (
                prop_data.get("type") == "multi_select"
                and prop_name == "For which major or course?"
            ):
                extracted_properties[prop_name] = [
                    option.get("name", "")
                    for option in prop_data.get("multi_select", [])
                ]
            elif prop_data.get("type") == "select" and prop_name == "Who can apply?":
                extracted_properties[prop_name] = prop_data.get("select", {}).get(
                    "name", ""
                )
            elif (
                prop_data.get("type") == "multi_select"
                and prop_name == "What do I get?"
            ):
                extracted_properties[prop_name] = [
                    option.get("name", "")
                    for option in prop_data.get("multi_select", [])
                ]
            elif (
                prop_data.get("type") == "date"
                and prop_name == "Until when can I apply?"
            ):
                extracted_properties[prop_name] = prop_data.get("date", {}).get(
                    "start", ""
                )
            elif prop_name == "PublicURL":
                extracted_properties[prop_name] = prop_data.get("rich_text", [{}])[
                    0
                ].get("plain_text", "")

        # Get cover image URL
        cover_image_url = page.get("cover", {}).get("file", {}).get("url", "")
        if cover_image_url.lower().startswith(("http://", "https://")):
            extracted_properties["cover_image_url"] = cover_image_url

        return extracted_properties
    except Exception as e:
        print(f"An error occurred while extracting page properties: {e}")
        return {}


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
                    page_properties = extract_page_properties(page_id)
                    try:
                        structured_message = clean_and_structure_content(
                            content, page_properties
                        )
                    except Exception as e:
                        print(f"Error in clean_and_structure_content: {e}")
                        structured_message = content  # Fallback to original content

                    notion_page_url = (
                        page_properties.get("PublicURL")
                        or f"https://www.notion.so/{page_id.replace('-', '')}"
                    )
                    cover_image_url = page_properties.get("cover_image_url", "")

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
