from notion_helper_functions import get_database_id, update_notion_block
from notion_database_ops import (
    extract_row_details,
    extract_last_row_details,
)
from prompt_initial_user_bio import generate_short_bio

# Usage example
database_title = "Chilipepper DB"
database_id = get_database_id(database_title)

if database_id:
    last_row = extract_last_row_details(database_id)
    if last_row:
        print("Last row details:", last_row)

        short_bio = generate_short_bio(last_row)

        # Update the specified Notion block
        block_id = "9023cf823e194456afb8b1d4793e11e5"
        update_notion_block(block_id, short_bio)
    else:
        print("Failed to retrieve the last row from the database.")
else:
    print("Failed to retrieve the database ID.")
