import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Notion client with your integration token
api_key = os.getenv("NOTION_API_KEY")
if not api_key:
    raise ValueError(
        "No Notion API key found. Please set the NOTION_API_KEY environment variable."
    )

notion = Client(auth=api_key)

# Replace with the title of your Notion database
database_title = "Foundational Essays"


def get_database_id(database_title):
    try:
        response = notion.search(
            **{
                "query": database_title,
                "filter": {"property": "object", "value": "database"},
            }
        )
        results = response.get("results", [])
        if not results:
            raise ValueError(f"No database found with the title: {database_title}")

        # Assuming the first result is the database we're looking for
        database_id = results[0]["id"]
        return database_id
    except Exception as e:
        print(f"An error occurred while searching for the database: {e}")
        return None


def read_notion_database(database_id):
    results = []
    try:
        # Query the database
        response = notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "IsFoundational",  # Adjust according to your database's properties
                    "checkbox": {
                        "equals": True  # Only fetch entries where the checkbox is checked
                    },
                },
            }
        )

        results = response.get("results", [])
    except Exception as e:
        print(f"An error occurred: {e}")

    return results


def get_page_content(page_id):
    try:
        response = notion.blocks.children.list(block_id=page_id)
        results = response.get("results", [])
        return results
    except Exception as e:
        print(f"An error occurred while retrieving page content: {e}")
        return []


def get_block_children(block_id):
    try:
        response = notion.blocks.children.list(block_id=block_id)
        return response.get("results", [])
    except Exception as e:
        print(f"An error occurred while retrieving block children: {e}")
        return []


def extract_toggle_children_content(children):
    children_content = []
    for child in children:
        child_type = child["type"]
        if child_type == "paragraph":
            paragraph_text = " ".join(
                [
                    text_part["text"]["content"]
                    for text_part in child["paragraph"]["rich_text"]
                ]
            )
            children_content.append(paragraph_text)
        # Handle other child types as needed
    return children_content


def extract_toggle_content(blocks):
    toggle_content = {}
    for block in blocks:
        if block["type"] == "toggle":
            toggle_text = block["toggle"]["rich_text"][0]["text"]["content"]
            children = get_block_children(block["id"])
            children_content = extract_toggle_children_content(children)
            toggle_content[toggle_text] = children_content
    return toggle_content


def main():
    database_id = get_database_id(database_title)
    if not database_id:
        print("Failed to retrieve the database ID.")
        return

    print(f"Database ID: {database_id}")

    database_entries = read_notion_database(database_id)

    if not database_entries:
        print("No entries found or there was an error retrieving the database.")

    for entry in database_entries:
        properties = entry.get("properties", {})
        # Extract and print the title or any other relevant properties
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )
        print(f"Title: {title}")

        # Get the page content for each entry
        page_id = entry.get("id")
        page_content = get_page_content(page_id)
        toggle_content = extract_toggle_content(page_content)

        foundational_essay = []
        for toggle_title, children in toggle_content.items():
            print(f"Toggle: {toggle_title}")
            for child in children:
                print(f"  Child Content: {child}")
                foundational_essay.append(child)
                print(f"  Foundational Essay: {foundational_essay}")

        print(foundational_essay)


if __name__ == "__main__":
    main()
