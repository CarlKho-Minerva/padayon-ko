from notion_utils import (
    get_database_id,
    extract_user_profile,
    get_scholarship_summaries,
)
from prompt_optimize_query import optimize_query
from gemini_embedding import find_best_matches
from notion_handle_status import update_scholarship_status


def main():
    print("\n### Starting main process ###\n")

    print("\n### Obtaining database IDs ###\n")
    user_db_id = get_database_id("Chilipepper DB")
    scholarship_db_id = get_database_id("Scholarship List for Padayun Ko")

    print("\n### Extracting user profile ###\n")
    user_profile = extract_user_profile(user_db_id)
    if not user_profile:
        print("\n### No user profile found. Exiting process. ###\n")
        return

    print("\n### Optimizing search based on user profile ###\n")
    optimized_query = optimize_query(user_profile)

    print("\n### Retrieving scholarship summaries ###\n")
    scholarship_summaries = get_scholarship_summaries(scholarship_db_id)
    if not scholarship_summaries:
        print("\n### No scholarships found. Exiting process. ###\n")
        return

    print("\n### Finding best matches for the user ###\n")
    best_match_indices = find_best_matches(optimized_query, scholarship_summaries)

    print("\n### Updating the status of the top 3 matched scholarships ###\n")
    for index in best_match_indices:
        scholarship = scholarship_summaries[index]
        print(f"\n### Updating status for scholarship: {scholarship['title']} ###\n")
        update_scholarship_status(scholarship_db_id, scholarship["page_id"])


if __name__ == "__main__":
    main()
