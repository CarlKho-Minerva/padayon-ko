from notion_helper_functions import notion, get_database_id
from backend.AI_Features.user_bio.notion_database_ops import extract_last_row_details


def update_notion_block(block_id, content):
    try:
        notion.blocks.update(
            block_id=block_id,
            callout={"rich_text": [{"type": "text", "text": {"content": content}}]},
        )
        print("Block updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the block: {e}")
