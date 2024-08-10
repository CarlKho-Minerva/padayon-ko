from notion_helper_functions import get_database_id, update_notion_block
from notion_database_ops import (
    extract_row_details,
    extract_last_row_details,
)
from backend.AI_Features.scholarship_matching.prompt_user_query import (
    generate_short_bio,
)
from prompt_user_query import generate_query_string


database_title = "Chilipepper DB"
database_id = get_database_id(database_title)


if database_id:
    last_row = extract_last_row_details(database_id)
    if last_row:
        print("Last row details:", last_row)

        optimized_string_query = generate_query_string(last_row)
    else:
        print("Failed to retrieve the last row from the database.")
else:
    print("Failed to retrieve the database ID.")
