import os
from notion_client import Client

# Initialize the Notion client
notion = Client(auth=os.environ["NOTION_API_KEY"])


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


def update_notion_block(block_id, content):
    try:
        notion.blocks.update(
            block_id=block_id,
            callout={"rich_text": [{"type": "text", "text": {"content": content}}]},
        )
        print("Block updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the block: {e}")
