from notion_utils import (
    get_database_id,
    extract_user_profile,
    get_scholarship_summaries,
)
from prompt_optimize_query import optimize_query
from gemini_embedding import find_best_matches
from notion_handle_status import update_scholarship_status


def main():
    print("Starting main process")
    user_db_id = get_database_id("Chilipepper DB")
    scholarship_db_id = get_database_id("Scholarship List for Padayun Ko")

    user_profile = extract_user_profile(user_db_id)
    if not user_profile:
        return

    optimized_query = optimize_query(user_profile)

    scholarship_summaries = get_scholarship_summaries(scholarship_db_id)
    if not scholarship_summaries:
        return

    best_match_indices = find_best_matches(optimized_query, scholarship_summaries)

    # Update the status of the top 3 matched scholarships
    for index in best_match_indices:
        scholarship = scholarship_summaries[index]
        print(f"Updating status for scholarship: {scholarship['title']}")
        update_scholarship_status(scholarship_db_id, scholarship["page_id"])


if __name__ == "__main__":
    main()
