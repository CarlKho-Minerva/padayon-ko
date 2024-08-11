from notion_utils import get_database_id, monitor_notion_database
from config import DATABASE_TITLE

if __name__ == "__main__":
    database_id = get_database_id(DATABASE_TITLE)
    if database_id:
        monitor_notion_database(database_id)
    else:
        print("Failed to get database ID.")
