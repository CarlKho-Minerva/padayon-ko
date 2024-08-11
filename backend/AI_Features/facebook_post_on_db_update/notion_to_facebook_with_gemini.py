from notion_client import Client
import requests
import os
import re
import google.generativeai as genai

FACEBOOK_ACCESS_TOKEN = "EAALn51qddPIBO3vVPEbS9sB1bdLPMX2lkmBj0ZCNz7bEzlpstZAKnXPGeSzRYWUffXlGEzn5IZC75TLi3mWq233jZBTmoXVBtqIQ2qoCLDRMaoYP5XpyyY6y40ERZAsZAHJZCV78d2ZBke9YdFK1sVHH6FdJCsAWACQQH1essFTHFnAMoN5fWHIdml2B65ZCyAptCFSkqwDxZCbPZBNmphgT64EzvZByw0FZBGojBkMGc1Wzw"
PAGE_ID = "394193433777965"

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Retrieve the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")


# Function to clean and structure content using Gemini API
def clean_and_structure_content(content):
    # Define the prompt for the Gemini API
    prompt = f"""
    Pretend to be an expert Facebook Social Media Manager. Clean and structure the following content for a Facebook post. Ensure the information is easy to skim through and includes clear sections. DO NOT USE ASTERISKS.

    Content:
    {content}

    Structure:
    - Just use proper spacing.
    - Provide a clear and concise summary - enough so that their interests will be piqued but make sure it's also informative.
    - Don't try to bold it because Facebook does not render bold.
    - Don't use emojis too much it will come off as scammy.
    """

    try:
        # Generate content using the Gemini model
        response = model.generate_content(prompt)
        structured_content = (
            response.text.strip()
        )  # Remove leading and trailing whitespace
        return structured_content
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return content  # Return the original content in case of an error


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


# Function to download an image from a URL
def download_image(image_url):
    if not image_url:
        print("No image URL provided.")
        return None
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"An error occurred while downloading the image: {e}")
        return None


# Function to upload an image to Facebook
def upload_facebook_image(image_data, access_token):
    url = f"https://graph.facebook.com/me/photos"
    payload = {"access_token": access_token}
    files = {"source": ("cover_image.jpg", image_data, "image/jpeg")}
    response = requests.post(url, data=payload, files=files)
    return response.json()


# Function to create a Facebook post with an image
def create_facebook_post(message, access_token, page_id, image_id=None):
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "access_token": access_token}
    if image_id:
        payload["object_attachment"] = image_id
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

                content = " ".join([extract_text_from_block(block) for block in blocks])
                content = re.sub(r"[^\w\s]", "", content)  # Strip special characters
                print(f"Content extracted from Notion blocks: {content}")

                if content:
                    # Clean and structure the content using Gemini API
                    structured_message = clean_and_structure_content(content)

                    # Get Notion page URL and cover image
                    notion_page_url, cover_image_url = fetch_page_properties(page_id)
                    if not notion_page_url:
                        notion_page_url = f"https://www.notion.so/{page_id.replace('-', '')}"  # Default URL if PublicURL is not available

                    # Print URL for debugging
                    print(f"Cover Image URL: {cover_image_url}")

                    # Download cover image
                    cover_image_data = download_image(cover_image_url)

                    # Upload cover image to Facebook and get image ID
                    facebook_image_id = None
                    if cover_image_data:
                        facebook_image_response = upload_facebook_image(
                            cover_image_data, FACEBOOK_ACCESS_TOKEN
                        )
                        facebook_image_id = facebook_image_response.get("id")

                    # Append the Notion page URL to the end of the structured message
                    final_message = f"{structured_message}\n\nLink to more details: {notion_page_url}"

                    # Replace with actual access token and page ID
                    access_token = FACEBOOK_ACCESS_TOKEN
                    page_id = PAGE_ID
                    # Create Facebook post
                    post_response = create_facebook_post(
                        final_message, access_token, page_id, facebook_image_id
                    )
                    print("Facebook post response:", post_response)

    except Exception as e:
        print(f"An error occurred while monitoring Notion database: {e}")


if __name__ == "__main__":
    database_title = "Scholarship List for Padayun Ko"
    database_id = get_database_id(database_title)
    if database_id:
        monitor_notion_database(database_id)
    else:
        print("Failed to get database ID.")
