from config import model


def format_essay(essay):
    formatPrompt = f"""
    Remove any markdown indicators and ensure it's in plain text format. Format this essay with proper paragraph structure and punctuation.

    Essay: {essay}

    Formatted essay:
    """
    response = model.generate_content(formatPrompt)
    return response.text
