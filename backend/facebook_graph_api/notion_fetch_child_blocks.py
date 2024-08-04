from notion_client import Client
import os

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_API_KEY"))


def extract_text_from_block(block):
    block_type = block.get("type")
    text_parts = []

    if block_type == "paragraph":
        rich_text = block.get("paragraph", {}).get("rich_text", [])
        text_parts = [text.get("plain_text", "") for text in rich_text]
    elif block_type == "heading_1":
        rich_text = block.get("heading_1", {}).get("rich_text", [])
        text_parts = [text.get("plain_text", "") for text in rich_text]
    elif block_type == "heading_2":
        rich_text = block.get("heading_2", {}).get("rich_text", [])
        text_parts = [text.get("plain_text", "") for text in rich_text]
    elif block_type == "heading_3":
        rich_text = block.get("heading_3", {}).get("rich_text", [])
        text_parts = [text.get("plain_text", "") for text in rich_text]
    elif block_type == "bulleted_list_item":
        rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
        text_parts = [text.get("plain_text", "") for text in rich_text]
        return f"- {' '.join(text_parts)}"  # Proper bullet point formatting
    elif block_type == "numbered_list_item":
        rich_text = block.get("numbered_list_item", {}).get("rich_text", [])
        text_parts = [text.get("plain_text", "") for text in rich_text]
        return f"1. {' '.join(text_parts)}"  # Numbered list formatting
    elif block_type == "to_do":
        rich_text = block.get("to_do", {}).get("rich_text", [])
        text_parts = [text.get("plain_text", "") for text in rich_text]
        checked = block.get("to_do", {}).get("checked", False)
        return (
            f"- [x] {' '.join(text_parts)}"
            if checked
            else f"- [ ] {' '.join(text_parts)}"
        )

    return " ".join(text_parts)


# Function to fetch all child blocks of a database item as plain text
def fetch_all_child_blocks_as_text(page_id):
    all_text = []
    try:
        block_children = notion.blocks.children.list(block_id=page_id)
        while block_children:
            blocks = block_children.get("results", [])
            for block in blocks:
                # Print block data for debugging
                print(f"Block data: {block}")
                block_text = extract_text_from_block(block)
                if block_text:
                    all_text.append(block_text)
            if block_children.get("next_cursor"):
                block_children = notion.blocks.children.list(
                    block_id=page_id, start_cursor=block_children.get("next_cursor")
                )
            else:
                break
    except Exception as e:
        print(f"An error occurred while fetching child blocks: {e}")
    return "\n".join(all_text)


# Test the function with a specific page ID
if __name__ == "__main__":
    # Replace with your actual page ID
    test_page_id = "4a7a4f9ce3ae49a1873a7baa70a0b178"
    text_content = fetch_all_child_blocks_as_text(test_page_id)
    print(text_content)
