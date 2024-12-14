import os
from dotenv import load_dotenv
from app import app

# Clear any existing environment variable
os.environ.pop("GEMINI_API_KEY", None)

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
