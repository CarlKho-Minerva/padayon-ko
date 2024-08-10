# UNCOMMENT TRANSLATES ONCE DEVELOPED

import os
import google.generativeai as genai
from dotenv import load_dotenv

# from google.cloud import translate_v2 as translate
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Clear any existing environment variable
os.environ.pop("GEMINI_API_KEY", None)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="gemini_api_key")

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
)


# def detect_and_translate(text, target_language="en"):
#     if isinstance(text, bytes):
#         text = text.decode("utf-8")
#     detection = translate_client.detect_language(text)
#     if detection["language"] != target_language:
#         result = translate_client.translate(text, target_language=target_language)
#         return result["translatedText"]
#     return text


# def translate_to_english(text, target_language="en"):
#     if isinstance(text, bytes):
#         text = text.decode("utf-8")
#     result = translate_client.translate(text, target_language=target_language)
#     return result["translatedText"]


def clean_and_remove_fillers(userInput):
    cleanPrompt = f"""
    Clean up this text by removing filler words, stammering, and repetitions. Maintain the original meaning and key information.

    Input: {userInput}

    Output:
    """
    response = model.generate_content(cleanPrompt)
    return response.text


def refine_and_optimize_essay(essay, prompt_type):
    refinePrompt = f"""
    Refine and optimize this essay for a scholarship application. Tailor it to the "{prompt_type}" prompt while maintaining the original tone and voice. Ensure it doesn't sound artificial and it being able to be read by an academic and professional audience but not lose character.

    Guidelines:
    1. Enhance the narrative structure
    2. Emphasize personal growth and challenges overcome
    3. Maintain authenticity and original voice
    4. Ensure relevance to the specific prompt
    5. Avoid clichés and overly formal language

    Essay: {essay}

    Refined essay:
    """
    response = model.generate_content(refinePrompt)
    return response.text


def format_essay(essay):
    formatPrompt = f"""
    Remove any markdown indicators and ensure it's in plain text format. Format this essay with proper paragraph structure and punctuation.

    Essay: {essay}

    Formatted essay:
    """
    response = model.generate_content(formatPrompt)
    return response.text


def process_tell_us_about_you_essay(userInput):
    prompt = f"""
    Enhance this "Tell Us About You" scholarship essay. Focus on:
    1. Personal challenges and how they were overcome
    2. Responsibilities taken on within family or community
    3. Significant achievements
    4. Future aspirations and their connection to past experiences

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_how_are_you_unique_essay(userInput):
    prompt = f"""
    Enhance this "How Are You Unique?" scholarship essay. Focus on:
    1. Unique aspects of background, identity, interests, or talents
    2. Significance of these unique qualities
    3. Specific examples demonstrating uniqueness
    4. How these qualities contribute to academic or personal goals

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_failure_and_learning_essay(userInput):
    prompt = f"""
    Enhance this "Tell Us About a Time You Failed and What You Learned From It" essay. Focus on:
    1. Description of the failure
    2. Impact of the failure
    3. Emotions and needs that arose from the experience
    4. Actions taken to address the failure
    5. Lessons learned and how they've been applied

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_academic_and_career_goals_essay(userInput):
    prompt = f"""
    Enhance this "What Are Your Academic and Career Goals?" essay. Focus on:
    1. Specific academic goals
    2. Career aspirations
    3. Challenges that shaped these goals
    4. Steps taken or planned to achieve these goals
    5. How these goals align with personal values or experiences

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_community_contribution_essay(userInput):
    prompt = f"""
    Enhance this "How Have You Contributed to Your Community?" essay. Focus on:
    1. Specific community service project or contribution
    2. Problem or challenge addressed
    3. Actions taken and individual role
    4. Impact on the community
    5. Personal growth and lessons learned

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_deserve_scholarship_essay(userInput):
    prompt = f"""
    Enhance this "Why Do You Deserve This Scholarship?" essay. Focus on:
    1. Personal qualities that make you a strong candidate
    2. Academic or extracurricular achievements
    3. Challenges overcome
    4. Future potential and how the scholarship will help
    5. Alignment with the scholarship's mission or values

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_scholarship_help_essay(userInput):
    prompt = f"""
    Enhance this "How Will This Scholarship Help You?" essay. Focus on:
    1. Specific ways the scholarship will be used
    2. Financial challenges or needs
    3. Academic or career goals supported by the scholarship
    4. Potential impact on your future
    5. How you plan to pay it forward or contribute to society

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_sports_impact_essay(userInput):
    prompt = f"""
    Enhance this "What Impact Has Sports Had on Your Life?" essay. Focus on:
    1. Specific sport or athletic activity
    2. Life lessons learned through sports
    3. Personal growth and character development
    4. Challenges overcome through sports
    5. How sports have influenced other areas of life

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_why_study_pursue_essay(userInput):
    prompt = f"""
    Enhance this "Why Do You Want to Study/Pursue [X]?" essay. Focus on:
    1. Specific field of study or career path
    2. Experiences that sparked interest in this field
    3. Relevant skills or knowledge already acquired
    4. Future goals related to this field
    5. Potential impact or contribution to the field

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_belief_challenged_essay(userInput):
    prompt = f"""
    Enhance this "Tell Us About a Time When You Had a Belief or Idea Challenged" essay. Focus on:
    1. Initial belief or idea
    2. Situation or experience that challenged this belief
    3. Thought process and emotions during the challenge
    4. How the belief or idea changed (if it did)
    5. Lessons learned or personal growth from this experience

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


DEBUG_MODE = True


def debug_print(message):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(message)


def process_essay(essay_type: str, user_input: str, needs_translation: bool) -> str:
    debug_print("\n### Initial Input\n")
    debug_print(f"Essay Type: {essay_type}\n")
    debug_print(f"User Input: {user_input}\n")
    debug_print(f"Needs Translation: {needs_translation}\n")

    # Translate if needed and checkbox is checked
    if needs_translation:
        user_input = detect_and_translate(user_input)
        debug_print("### Translating Input\n")
        debug_print(f"Translated Input: {user_input}\n")

    # Clean and remove fillers
    cleaned_essay = clean_and_remove_fillers(user_input)
    debug_print("### Cleaning and Removing Fillers\n")
    debug_print(f"Cleaned Essay: {cleaned_essay}\n")

    # Process based on essay type
    processing_functions = {
        "tell_us_about_you": process_tell_us_about_you_essay,
        "how_are_you_unique": process_how_are_you_unique_essay,
        "failure_and_learning": process_failure_and_learning_essay,
        "academic_and_career_goals": process_academic_and_career_goals_essay,
        "community_contribution": process_community_contribution_essay,
        "deserve_scholarship": process_deserve_scholarship_essay,
        "scholarship_help": process_scholarship_help_essay,
        "sports_impact": process_sports_impact_essay,
        "why_study_pursue": process_why_study_pursue_essay,
        "belief_challenged": process_belief_challenged_essay,
    }

    if essay_type in processing_functions:
        processed_essay = processing_functions[essay_type](cleaned_essay)
        debug_print("### Processing Essay\n")
        debug_print(f"Processed Essay: {processed_essay}\n")
    else:
        return "Invalid essay type"

    # Refine and optimize
    refined_essay = refine_and_optimize_essay(processed_essay, essay_type)
    debug_print("### Refining and Optimizing Essay\n")
    debug_print(f"Refined Essay: {refined_essay}\n")

    # Format
    final_essay = format_essay(refined_essay)
    debug_print("### Formatting Essay\n")
    debug_print(f"Final Essay: {final_essay}\n")

    return final_essay


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.json
    essay_type = data["essay_type"]
    user_input = data["essay_content"]
    needs_translation = data["needs_translation"]

    final_essay = process_essay(essay_type, user_input, needs_translation)

    return jsonify({"processed_essay": final_essay})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
