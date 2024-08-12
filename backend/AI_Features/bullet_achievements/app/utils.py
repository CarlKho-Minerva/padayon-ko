import google.generativeai as genai
import os
from dotenv import load_dotenv

DEBUG_MODE = True


def debug_print(message):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(message)


def configure_genai():
    # Clear any existing environment variable
    os.environ.pop("GEMINI_API_KEY", None)

    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the API key from environment variables
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    print(gemini_api_key)

    genai.configure(api_key=gemini_api_key)


def get_model():
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro", safety_settings=safety_settings
    )
    return model


model = get_model()
