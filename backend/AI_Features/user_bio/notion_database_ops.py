from notion_helper_functions import notion, get_database_id


def extract_row_details(db_title):
    """
    # Sample usage
    # Get the database ID
    database_title = "Chilipepper DB"
    database_id = get_database_id(database_title)

    if database_id:
        results = extract_row_details(database_id)
        for row in results:
            print(row)
    else:
        print("Failed to retrieve the database ID.")
    """
    try:
        # Query the database
        profile_db_id = get_database_id(db_title)
        response = notion.databases.query(database_id=profile_db_id)

        # Extract and process the results
        rows = []
        for page in response.get("results", []):
            properties = page.get("properties", {})

            row = {
                "email": properties.get("title", {})
                .get("title", [{}])[0]
                .get("plain_text", ""),
                "name": properties.get("name", {})
                .get("rich_text", [{}])[0]
                .get("plain_text", ""),
                "career": properties.get("career", {})
                .get("rich_text", [{}])[0]
                .get("plain_text", ""),
                "degree": properties.get("degree", {})
                .get("rich_text", [{}])[0]
                .get("plain_text", ""),
                "achievement": properties.get("achievement", {})
                .get("rich_text", [{}])[0]
                .get("plain_text", ""),
                "ai": properties.get("ai", {})
                .get("rich_text", [{}])[0]
                .get("plain_text", ""),
            }

            rows.append(row)

        return rows
    except Exception as e:
        print(f"An error occurred while extracting row details: {e}")
        return []


def extract_last_row_details(database_id):
    try:
        # Query the database and sort by last edited time in descending order
        response = notion.databases.query(
            database_id=database_id,
            sorts=[{"property": "last_edited_time", "direction": "descending"}],
            page_size=1,  # We only need the last row
        )

        # Extract and process the result
        results = response.get("results", [])
        if not results:
            print("No rows found in the database.")
            return None

        page = results[0]
        properties = page.get("properties", {})

        row = {
            "email": properties.get("title", {})
            .get("title", [{}])[0]
            .get("plain_text", ""),
            "name": properties.get("name", {})
            .get("rich_text", [{}])[0]
            .get("plain_text", ""),
            "career": properties.get("career", {})
            .get("rich_text", [{}])[0]
            .get("plain_text", ""),
            "degree": properties.get("degree", {})
            .get("rich_text", [{}])[0]
            .get("plain_text", ""),
            "achievement": properties.get("achievement", {})
            .get("rich_text", [{}])[0]
            .get("plain_text", ""),
            "ai": properties.get("ai", {})
            .get("rich_text", [{}])[0]
            .get("plain_text", ""),
        }

        return row
    except Exception as e:
        print(f"An error occurred while extracting row details: {e}")
        return None
