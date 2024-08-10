from extract_db_row_props import extract_row_details
from prompt_initial_user_bio import generate_short_bio

# Get the database ID
database_title = "Chilipepper DB"
database_id = extract_row_details(database_title)

if database_id:
    for row in database_id:
        bio = generate_short_bio(row)
        print(bio)
