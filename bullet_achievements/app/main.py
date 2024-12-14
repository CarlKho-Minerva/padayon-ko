from flask import Flask, render_template, request, jsonify
import os
from clean_input import clean_and_remove_fillers, translate_and_clean
from extract_info import extract_key_info
from structure_achievement import structure_achievement
from generate_content import generate_bullet_point, generate_detailed_description
from refine_output import (
    refine_and_optimize_scholarship,
    separate_bullet_and_description,
)
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
        bullet, description = process_achievement(
            achievement_description, is_english, separate_output=True
        )
        return jsonify({"bullet": bullet, "description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_achievement(userInput, isEnglish=True, separate_output=False):
    debug_print("\n### Input Processing\n")
    debug_print(
        f"Input: {userInput}, Language: {'English' if isEnglish else 'Non-English'}\n"
    )

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
    detailedDescription = generate_detailed_description(
        bulletPoint, structuredAchievement
    )
    debug_print(f"Detailed Description: {detailedDescription}\n")

    debug_print("### Refining Achievement\n")
    refinedAchievement = refine_and_optimize_scholarship(
        bulletPoint, detailedDescription, userInput
    )
    debug_print(f"Refined Achievement: {refinedAchievement}\n")

    if separate_output:
        debug_print("### Separating Bullet and Description\n")
        refinedBullet, optimizedDescription = separate_bullet_and_description(
            refinedAchievement
        )
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
