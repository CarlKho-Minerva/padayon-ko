File structure:

app/
├── main.py
├── clean_input.py
├── extract_info.py
├── structure_achievement.py
├── generate_content.py
├── refine_output.py
├── utils.py
└── templates/
    └── index.html

File contents:

1. main.py

```python
from flask import Flask, render_template, request, jsonify
import os
from clean_input import clean_and_remove_fillers, translate_and_clean
from extract_info import extract_key_info
from structure_achievement import structure_achievement
from generate_content import generate_bullet_point, generate_detailed_description
from refine_output import refine_and_optimize, separate_bullet_and_description
from utils import debug_print, configure_genai

app = Flask(__name__)

# Configure Gemini AI
configure_genai()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_resume():
    data = request.json
    achievement_description = data.get("achievement", "")
    is_english = data.get("isEnglish", True)

    try:
        bullet, description = process_achievement(achievement_description, is_english, separate_output=True)
        return jsonify({"bullet": bullet, "description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_achievement(userInput, isEnglish=True, separate_output=False):
    debug_print("\n### Input Processing\n")
    debug_print(f"Input: {userInput}, Language: {'English' if isEnglish else 'Non-English'}\n")

    if isEnglish:
        debug_print("### Cleaning Input\n")
        cleanedInput = clean_and_remove_fillers(userInput)
    else:
        debug_print("### Translating and Cleaning Input\n")
        cleanedInput = translate_and_clean(userInput)
    debug_print(f"Cleaned Input: {cleanedInput}\n")

    debug_print("### Extracting Information\n")
    extractedInfo = extract_key_info(cleanedInput)
    debug_print(f"Extracted Info: {extractedInfo}\n")

    debug_print("### Structuring Achievement\n")
    structuredAchievement = structure_achievement(extractedInfo)
    debug_print(f"Structured Achievement: {structuredAchievement}\n")

    debug_print("### Generating Bullet Point\n")
    bulletPoint = generate_bullet_point(structuredAchievement)
    debug_print(f"Bullet Point: {bulletPoint}\n")

    debug_print("### Generating Detailed Description\n")
    detailedDescription = generate_detailed_description(bulletPoint, structuredAchievement)
    debug_print(f"Detailed Description: {detailedDescription}\n")

    debug_print("### Refining Achievement\n")
    refinedAchievement = refine_and_optimize(bulletPoint, detailedDescription, userInput)
    debug_print(f"Refined Achievement: {refinedAchievement}\n")

    if separate_output:
        debug_print("### Separating Bullet and Description\n")
        refinedBullet, optimizedDescription = separate_bullet_and_description(refinedAchievement)
        debug_print(f"Refined Bullet: {refinedBullet}\n")
        debug_print(f"Optimized Description: {optimizedDescription}\n")
        return refinedBullet, optimizedDescription
    else:
        debug_print("### Combined Refined Text\n")
        debug_print(f"Refined Text: {refinedAchievement}\n")
        return refinedAchievement

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
```

2. clean_input.py

```python
from utils import get_model

def clean_and_remove_fillers(userInput):
    model = get_model()
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

def translate_and_clean(nonEnglishInput):
    model = get_model()
    translatePrompt = f"""
    Translate this text to English, then clean it up by improving clarity and grammar. Ensure it's well-structured while maintaining the original meaning and key information.

    Input: {nonEnglishInput}

    Output:
    """
    response = model.generate_content(translatePrompt)
    return response.text
```

3. extract_info.py

```python
from utils import get_model

def extract_key_info(cleanedInput):
    model = get_model()
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
```

4. structure_achievement.py

```python
from utils import get_model

def structure_achievement(extractedInfo):
    model = get_model()
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
```

5. generate_content.py

```python
from utils import get_model

def generate_bullet_point(structuredAchievement):
    model = get_model()
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

def generate_detailed_description(bulletPoint, structuredAchievement):
    model = get_model()
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
```

6. refine_output.py

```python
from utils import get_model

def refine_and_optimize(bulletPoint, detailedDescription, rawInput):
    model = get_model()
    refinePrompt = f"""
    As an expert copywriter, refine and optimize this achievement for a scholarship application. Ensure it's impactful, concise, and tailored for scholarships while maintaining the original tone and authenticity. Still maintain professional but friendly academic tone. Avoid making it sound AI-generated. You can refer to the `raw_input` variable for the original tone.

    Raw Input: {rawInput}

    Current Bullet: {bulletPoint}

    Current Description: {detailedDescription}

    Remove markdown as we need it in a plain text format.

    Provide a refined version of both the bullet point and description, separated by a tilde (~):

    Refined Bullet:
    •

    ~

    Optimized Description:
    """
    response = model.generate_content(refinePrompt)
    return response.text

def separate_bullet_and_description(refined_text):
    parts = refined_text.split("~")
    bullet = parts[0].strip().split("\n")[-1]  # Get the last line of the first part
    description = parts[1].strip()
    return bullet, description
```

7. utils.py

```python
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
```
