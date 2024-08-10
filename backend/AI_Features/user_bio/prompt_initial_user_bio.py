import google.generativeai as genai
import os
import dotenv

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = none
    tools="code_execution",
)


def generate_short_bio(user_data):
    prompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are a professional bio writer specializing in crafting concise and engaging bios for professionals in technology fields.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    You will be provided with a JSON object containing a user's information. Use this information to generate a short professional bio.
    1. Extract the relevant details from the JSON object, including name, career aspirations, degree, and any notable achievements related to their field.
    2. Focus on highlighting technical skills and passion for the field.
    3. Craft a bio that is between 40 and 60 words in length.
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following:
    1. Do: Write in the third person.
    2. Do: Maintain a professional and positive tone.
    3. Don't: Include any personal information beyond what is provided in the JSON object.
    4. Don't: Invent or exaggerate any details.
    </CONSTRAINTS>

    <OUTPUT_FORMAT>
    Output a single string containing the short professional bio.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples:
    1. Example #1
        Input: {{"email": "", "name": "Alice", "career": "Software Engineer", "degree": "Computer Science", "achievement": "Developed a mobile app with over 10,000+ downloads", "ai": "Passionate about using AI to improve healthcare."}}
        Output: "Alice is an aspiring Software Engineer with a degree in Computer Science. Having developed a successful mobile app with over 10,000 downloads, she is passionate about leveraging technology, particularly AI, to create impactful solutions in the healthcare industry."

    2. Example #2
        Input: {{"email": "", "name": "Bob", "career": "Data Scientist", "degree": "Statistics", "achievement": "Won first place in a university data mining competition", "ai": "Interested in applying machine learning to financial markets."}}
        Output: "Bob is a driven Data Scientist with a strong foundation in Statistics. His analytical prowess earned him first place in a university data mining competition. He aims to apply his machine learning expertise to the financial markets."
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    Generate a professional bio, keeping it concise, relevant, and within the word limit.
    </RECAP>

    Now, generate a bio using this information: {user_data}
    """
    response = model.generate_content(prompt)
    return response.text


print(
    generate_short_bio(
        '{{"email": "john.doe@example.com", "name": "John Doe", "career": "Data Scientist", "degree": "Statistics", "achievement": "Published a research paper on machine learning algorithms", "ai": "Enthusiastic about leveraging AI for climate change solutions."}}'
    )
)
