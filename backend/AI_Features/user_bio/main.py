from notion_helper_functions import get_database_id, update_notion_block
from notion_database_ops import (
    extract_last_row_details,
)
from prompt_initial_user_bio import generate_short_bio

database_title = "Chilipepper DB"
block_id = "9023cf823e194456afb8b1d4793e11e5"

print("\n### Starting the process to update the Notion block... ###\n")

print("\n### Step 1: Obtaining the database ID for the title:", database_title, "###\n")
database_id = get_database_id(database_title)

if database_id:
    print("\n### Successfully obtained the database ID:", database_id, "###\n")

    print("\n### Step 2: Searching for the last row in the database... ###\n")
    last_row = extract_last_row_details(database_id)

    if last_row:
        print("\n### Successfully found the last row details:", last_row, "###\n")

        print("\n### Step 3: Generating a short bio from the last row details... ###\n")
        short_bio = generate_short_bio(last_row)
        print("\n### Generated short bio:", short_bio, "###\n")

        print("\n### Step 4: Updating the Notion block with the generated bio... ###\n")
        update_notion_block(block_id, short_bio)
        print("\n### Successfully updated the Notion block! ###\n")
        print("\n### Successfully generated custom user bio with Gemini API! ###\n")
    else:
        print("\n### Failed to retrieve the last row from the database. ###\n")
else:
    print("\n### Failed to retrieve the database ID. ###\n")
