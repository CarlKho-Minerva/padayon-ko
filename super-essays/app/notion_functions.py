import pandas as pd
from gemini_functions import embed_content


def get_database_id(notion, database_title):
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


def query_notion_database(notion, database_id, filter_condition=None):
    query_params = {"database_id": database_id}
    if filter_condition:
        query_params["filter"] = filter_condition
    try:
        response = notion.databases.query(**query_params)
        return response.get("results", [])
    except Exception as e:
        print(f"An error occurred while querying the database: {e}")
        return []


def get_page_content(notion, page_id):
    try:
        response = notion.blocks.children.list(block_id=page_id)
        return response.get("results", [])
    except Exception as e:
        print(f"An error occurred while retrieving page content: {e}")
        return []


def extract_toggle_content(notion, blocks):
    toggle_content = {}
    for block in blocks:
        if block["type"] == "toggle":
            toggle_text = block["toggle"]["rich_text"][0]["text"]["content"]
            children = notion.blocks.children.list(block_id=block["id"]).get(
                "results", []
            )
            children_content = [
                " ".join(
                    [
                        text_part["text"]["content"]
                        for text_part in child["paragraph"]["rich_text"]
                    ]
                )
                for child in children
                if child["type"] == "paragraph"
            ]
            toggle_content[toggle_text] = children_content
    return toggle_content


def process_foundational_essays(notion, database_id):
    filter_condition = {"property": "IsFoundational", "checkbox": {"equals": True}}
    entries = query_notion_database(notion, database_id, filter_condition)
    essays = []
    for entry in entries:
        properties = entry.get("properties", {})
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )
        page_content = get_page_content(notion, entry.get("id"))
        toggle_content = extract_toggle_content(notion, page_content)
        for toggle_title, children in toggle_content.items():
            essay_text = "\n".join(children)
            essays.append({"title": toggle_title, "content": essay_text})
    df = pd.DataFrame(essays)
    df["Embeddings"] = df.apply(
        lambda row: embed_content(row["title"], row["content"]), axis=1
    )
    return df


def process_student_achievements(notion, database_id):
    entries = query_notion_database(notion, database_id)
    achievements = []
    for entry in entries:
        properties = entry.get("properties", {})
        title = (
            properties.get("Name", {})
            .get("title", [{}])[0]
            .get("text", {})
            .get("content", "No Title")
        )
        achievements.append({"title": title, "content": title})
    df = pd.DataFrame(achievements)
    df["Embeddings"] = df.apply(
        lambda row: embed_content(row["title"], row["content"]), axis=1
    )
    return df
