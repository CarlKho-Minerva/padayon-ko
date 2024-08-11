import os
import google.generativeai as genai

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")


def clean_and_structure_content(content):
    prompt = f"""
    Pretend to be an expert Facebook Social Media Manager. Clean and structure the following content for a Facebook post. Ensure the information is easy to skim through and includes clear sections. DO NOT USE ASTERISKS.

    Content:
    {content}

    Structure:
    - Just use proper spacing.
    - Provide a clear and concise summary - enough so that their interests will be piqued but make sure it's also informative.
    - Don't try to bold it because Facebook does not render bold.
    - Don't use emojis too much it will come off as scammy.
    """

    try:
        response = model.generate_content(prompt)
        structured_content = response.text.strip()
        return structured_content
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return content
