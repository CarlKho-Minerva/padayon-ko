from config import model


def clean_and_remove_fillers(userInput):
    cleanPrompt = f"""
    Clean up this text by removing filler words, stammering, and repetitions. Maintain the original meaning and key information.

    Input: {userInput}

    Output:
    """
    response = model.generate_content(cleanPrompt)
    return response.text
