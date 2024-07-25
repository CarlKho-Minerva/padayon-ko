import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Clear any existing environment variable
os.environ.pop("GEMINI_API_KEY", None)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro", safety_settings=safety_settings
)


def cleanup_text(user_input):
    prompt = f"""
    Clean up the following text by improving grammar, sentence structure, and removing filler words:
    1. Correct grammatical errors
    2. Improve sentence structure for clarity
    3. Remove filler words and redundant phrases
    4. Maintain the original meaning of the text
    5. Do not add new information or change the content

    Original text: {user_input}

    Cleaned up version:
    """
    response = model.generate_content(prompt)
    return response.text


def translate_to_english(user_input):
    prompt = f"""
    Translate the following text to English:
    1. Detect the language of the input text
    2. Accurately translate the text to English
    3. Preserve the original meaning and tone
    4. Maintain any cultural nuances where possible

    Original text: {user_input}

    English translation:
    """
    response = model.generate_content(prompt)
    return response.text


def craft_origin_story(user_input, story_length):
    prompt = f"""
    Craft a compelling origin story based on the following accomplishment, suitable for self-marketing in various social functions. The student must personally relate and journey listeners to their life. The story should be {story_length} in length.

    1. Identify the key elements of the accomplishment
    2. Structure the story with a clear beginning, middle, and end
    3. Highlight the challenges and growth experienced
    4. Emphasize personal motivation and impact
    5. Use vivid language to engage the listener/reader
    6. Ensure the story is authentic and does not exaggerate
    7. Tailor the story length to be {story_length}. Choose one only: approximately 30 seconds long for short (1 paragraph), 1 minute long for medium (2 paragraphs), 3 minutes long for long (3 paragraphs))

    Accomplishment: {user_input}

    Crafted origin story:
    """
    response = model.generate_content(prompt)
    return response.text


def optimize_for_marketing(user_input):
    prompt = f"""
    Optimize the following origin story for effective self-marketing in social functions but remain human and conversational:

    1. Highlight qualities that make the individual stand out (e.g., leadership, innovation, perseverance)
    2. Emphasize the impact and potential future contributions
    3. Ensure the language is engaging and memorable
    4. Include specific examples that demonstrate unique skills or experiences
    5. Align the content with common themes in personal branding (e.g., problem-solving, vision, adaptability)
    6. Maintain authenticity while presenting the accomplishments in the best light
    7. Make the story relatable and inspirational to the audience
    8. Remove any markdown. We need plain text output.
    9. Maintain first person POV and no-bullshit marketing-style talk. Just be very human and humble.

    Original story: {user_input}

    Optimized story for marketing:
    """
    response = model.generate_content(prompt)
    return response.text


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_story", methods=["POST"])
def process_story():
    data = request.json
    user_input = data["userInput"]
    is_english = data["isEnglish"]
    story_length = data["storyLength"]

    if not is_english:
        user_input = translate_to_english(user_input)

    cleaned_text = cleanup_text(user_input)
    origin_story = craft_origin_story(cleaned_text, story_length)
    optimized_story = optimize_for_marketing(origin_story)

    return jsonify({"result": optimized_story})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
