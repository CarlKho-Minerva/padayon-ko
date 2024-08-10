import google.generativeai as genai
import os
from dotenv import load_dotenv

# Clear any existing environment variable
os.environ.pop("GEMINI_API_KEY", None)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="gemini_api_key")
