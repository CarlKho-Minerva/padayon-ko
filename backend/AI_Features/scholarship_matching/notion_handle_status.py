from notion_utils import notion


def get_status_options(database_id):
    print(f"Retrieving status options for database ID: {database_id}")
    database = notion.databases.retrieve(database_id=database_id)
    status_property = database["properties"].get("Status")
    if status_property and status_property["type"] == "status":
        options = status_property["status"]["options"]
        print(f"Status options retrieved.")
        return options
    print("No status options found.")
    return None


def update_scholarship_status(database_id, page_id):
    print(
        f"Updating scholarship status for page ID: {page_id} in database ID: {database_id}"
    )
    status_options = get_status_options(database_id)
    if not status_options:
        print("Error: Could not find Status options in the database.")
        return

    in_progress_option = next(
        (
            option
            for option in status_options
            if option["name"].lower() == "in progress"
        ),
        None,
    )
    if not in_progress_option:
        print("Error: Could not find 'In Progress' status option.")
        return

    try:
        notion.pages.update(
            page_id=page_id,
            properties={"Status": {"status": {"id": in_progress_option["id"]}}},
        )
        print(f"Successfully updated status for page ID: {page_id}")
    except Exception as e:
        print(f"Error updating status for page ID {page_id}: {e}")
