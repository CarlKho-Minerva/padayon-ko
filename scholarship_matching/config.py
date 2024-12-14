import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CACHE_FILE = "scholarship_cache.json"
CACHE_EXPIRY_DAYS = 7
