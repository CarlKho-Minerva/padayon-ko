import os
from dotenv import load_dotenv
from app import app

if __name__ == "__main__":
    # Clear any existing environment variable
    os.environ.pop("GEMINI_API_KEY", None)

    # Load environment variables from .env file
    load_dotenv()

    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
