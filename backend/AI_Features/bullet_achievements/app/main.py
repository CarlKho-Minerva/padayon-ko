from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

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


# Step 1: Clean and prepare input
def clean_and_remove_fillers(userInput):
    cleanPrompt = f"""
    Clean up this text by removing filler words, stammering, and repetitions. Maintain the original meaning and key information.

    Input: "Um, so like, I started this, uh, coding club at my school last year and we, we managed to get about 30 members and, you know, organized a hackathon."

    Output: "I started a coding club at my school last year. We managed to get about 30 members and organized a hackathon."

    Now clean up this text:
    Input: {userInput}

    Output:
    """
    response = model.generate_content(cleanPrompt)
    return response.text


# Step 1 (Alternative): Translate and clean non-English input
def translate_and_clean(nonEnglishInput):
    translatePrompt = f"""
    Translate this text to English, then clean it up by improving clarity and grammar. Ensure it's well-structured while maintaining the original meaning and key information.

    Input: {nonEnglishInput}

    Output:
    """
    response = model.generate_content(translatePrompt)
    return response.text


# Step 2: Extract key information
def extract_key_info(cleanedInput):
    extractPrompt = f"""
    Extract key information about achievements from this input. Focus on:
    - Specific roles and responsibilities
    - Quantifiable results (numbers, percentages, etc.)
    - Impact on community or organization
    - Skills developed or demonstrated
    - Challenges overcome
    - Time frame and context of the achievement

    Input: "I started a coding club at my school last year. We managed to get about 30 members and organized a hackathon."

    Output:
    - Role: Founder of coding club
    - Time frame: Last year
    - Quantifiable result: 30 members
    - Achievement: Organized a hackathon
    - Skills: Leadership, organization, coding
    - Impact: Increased coding interest in school

    Now extract key information from this input:
    Input: {cleanedInput}

    Output:
    """
    response = model.generate_content(extractPrompt)
    return response.text


# Step 3: Structure achievement (X-Y-Z formula)
def structure_achievement(extractedInfo):
    structurePrompt = f"""
    Structure this achievement using the X-Y-Z formula: "Accomplished [X] as measured by [Y], by doing [Z]". Provide a comprehensive yet concise structure.

    Input:
    - Role: Founder of coding club
    - Time frame: Last year
    - Quantifiable result: 30 members
    - Achievement: Organized a hackathon
    - Skills: Leadership, organization, coding
    - Impact: Increased coding interest in school

    Output:
    X (Accomplishment): Founded and grew a successful coding club
    Y (Measurement): Attracted 30 members and organized a school-wide hackathon
    Z (Method): Leveraged leadership and organizational skills to create engaging coding activities and events

    Now structure this achievement:
    Input: {extractedInfo}

    Output:
    X (Accomplishment):
    Y (Measurement):
    Z (Method):
    """
    response = model.generate_content(structurePrompt)
    return response.text


# Step 4: Generate resume bullet point
def generate_bullet_point(structuredAchievement):
    bulletPrompt = f"""
    Create a concise, impactful bullet point summary of this achievement using the X-Y-Z formula. Start with a strong action verb, include quantifiable results, and hint at broader significance.

    Input:
    X (Accomplishment): Founded and grew a successful coding club
    Y (Measurement): Attracted 30 members and organized a school-wide hackathon
    Z (Method): Leveraged leadership and organizational skills to create engaging coding activities and events

    Output:
    • Spearheaded school's first coding club, growing membership to 30 students and orchestrating a successful hackathon, fostering a culture of innovation and tech literacy

    Now create a bullet point for this achievement:
    Input: {structuredAchievement}

    Output:
    •
    """
    response = model.generate_content(bulletPrompt)
    return response.text


# Step 5: Generate detailed description
def generate_detailed_description(bulletPoint, structuredAchievement):
    descriptionPrompt = f"""
    Expand this bullet point into a detailed description. Include:
    - Context and importance of the achievement
    - Specific actions taken and leadership demonstrated
    - Quantifiable impacts and results
    - Challenges overcome
    - Skills developed or applied
    - Relevance to future goals or field of study
    Keep it under 4 sentences and maintain a natural, non-AI tone.

    Input:
    Bullet: • Spearheaded school's first coding club, growing membership to 30 students and orchestrating a successful hackathon, fostering a culture of innovation and tech literacy
    Structure:
    X (Accomplishment): Founded and grew a successful coding club
    Y (Measurement): Attracted 30 members and organized a school-wide hackathon
    Z (Method): Leveraged leadership and organizational skills to create engaging coding activities and events

    Output:
    As a passionate coder, I noticed a lack of programming opportunities at my school and took the initiative to start our first-ever coding club. Despite initial skepticism from the administration, I persevered and grew our membership to 30 dedicated students through engaging weekly workshops and coding challenges. The highlight of our first year was organizing a school-wide hackathon, where teams developed innovative solutions to local community problems, showcasing our newly acquired skills and fostering a culture of tech enthusiasm. This experience not only honed my leadership and event planning abilities but also reinforced my commitment to making technology education more accessible to my peers.

    Now generate a detailed description for this achievement:
    Input:
    Bullet: {bulletPoint}
    Structure: {structuredAchievement}

    Output:
    """
    response = model.generate_content(descriptionPrompt)
    return response.text


# Step 6: Refine, optimize, and separate
def refine_and_optimize(bulletPoint, detailedDescription, rawInput):
    refinePrompt = f"""
    As an expert copywriter, refine and optimize this achievement for a scholarship application. Ensure it's impactful, concise, and tailored for scholarships while maintaining the original tone and authenticity. Still maintain professional but friendly academic tone. Avoid making it sound AI-generated. You can refer to the `raw_input` variable for the original tone.

    Raw Input: {rawInput}

    Current Bullet: {bulletPoint}

    Current Description: {detailedDescription}

    Provide a refined version of both the bullet point and description, separated by a tilde (~):

    Refined Bullet:
    •

    ~

    Optimized Description:
    """
    # Assuming model.generate_content is a placeholder for an actual API call or function that generates content based on the prompt
    response = model.generate_content(refinePrompt)
    return response.text


def separate_bullet_and_description(refined_text):
    parts = refined_text.split("~")
    bullet = parts[0].strip().split("\n")[-1]  # Get the last line of the first part
    description = parts[1].strip()
    return bullet, description


# Global variable to control debug mode

DEBUG_MODE = True


def debug_print(message):
    """Prints a debug message if DEBUG_MODE is True."""
    if DEBUG_MODE:
        print(message)


# Modify the process_achievement function to use debug_print with clear headers and spacing
def process_achievement(userInput, isEnglish=True, separate_output=False):
    debug_print("\n### Input Processing\n")
    debug_print(
        f"Input: {userInput}, Language: {'English' if isEnglish else 'Non-English'}\n"
    )

    if isEnglish:
        cleanedInput = clean_and_remove_fillers(userInput)
        debug_print("### Cleaning Input\n")
        debug_print(f"Cleaned Input: {cleanedInput}\n")
    else:
        cleanedInput = translate_and_clean(userInput)
        debug_print("### Translating and Cleaning Input\n")
        debug_print(f"Translated and Cleaned Input: {cleanedInput}\n")

    extractedInfo = extract_key_info(cleanedInput)
    debug_print("### Extracting Information\n")
    debug_print(f"Extracted Info: {extractedInfo}\n")

    structuredAchievement = structure_achievement(extractedInfo)
    debug_print("### Structuring Achievement\n")
    debug_print(f"Structured Achievement: {structuredAchievement}\n")

    bulletPoint = generate_bullet_point(structuredAchievement)
    debug_print("### Generating Bullet Point\n")
    debug_print(f"Bullet Point: {bulletPoint}\n")

    detailedDescription = generate_detailed_description(
        bulletPoint, structuredAchievement
    )
    debug_print("### Generating Detailed Description\n")
    debug_print(f"Detailed Description: {detailedDescription}\n")

    refinedAchievement = refine_and_optimize(
        bulletPoint, detailedDescription, userInput
    )
    debug_print("### Refining Achievement\n")
    debug_print(f"Refined Achievement: {refinedAchievement}\n")

    if separate_output:
        # Separate the refined bullet and description if separate_output is True
        refinedBullet, optimizedDescription = separate_bullet_and_description(
            refinedAchievement
        )
        debug_print("### Separating Bullet and Description\n")
        debug_print(f"Refined Bullet: {refinedBullet}\n")
        debug_print(f"Optimized Description: {optimizedDescription}\n")
        return refinedBullet, optimizedDescription
    else:
        # Return the combined refined text if separate_output is False
        debug_print("### Combined Refined Text\n")
        debug_print(f"Refined Text: {refinedAchievement}\n")
        return refinedAchievement


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_resume():
    data = request.json
    achievement_description = data.get("achievement", "")
    is_english = data.get("isEnglish", True)

    try:
        bullet, description = process_achievement(
            achievement_description, is_english, separate_output=True
        )
        return jsonify({"bullet": bullet, "description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
