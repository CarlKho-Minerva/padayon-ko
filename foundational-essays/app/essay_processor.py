from config import DEBUG_MODE
from text_cleaner import clean_and_remove_fillers
from essay_enhancer import process_essay_by_type, refine_and_optimize_essay
from essay_formatter import format_essay


def debug_print(message):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(message)


def process_essay(essay_type: str, user_input: str, needs_translation: bool) -> str:
    debug_print("\n### Initial Input\n")
    debug_print(f"Essay Type: {essay_type}\n")
    debug_print(f"User Input: {user_input}\n")
    debug_print(f"Needs Translation: {needs_translation}\n")

    # Clean and remove fillers
    cleaned_essay = clean_and_remove_fillers(user_input)
    debug_print("### Cleaning and Removing Fillers\n")
    debug_print(f"Cleaned Essay: {cleaned_essay}\n")

    # Process based on essay type
    processed_essay = process_essay_by_type(essay_type, cleaned_essay)
    debug_print("### Processing Essay\n")
    debug_print(f"Processed Essay: {processed_essay}\n")

    # Refine and optimize
    refined_essay = refine_and_optimize_essay(processed_essay, essay_type)
    debug_print("### Refining and Optimizing Essay\n")
    debug_print(f"Refined Essay: {refined_essay}\n")

    # Format
    final_essay = format_essay(refined_essay)
    debug_print("### Formatting Essay\n")
    debug_print(f"Final Essay: {final_essay}\n")

    return final_essay
