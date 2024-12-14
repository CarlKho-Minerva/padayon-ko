import os
import json
import google.generativeai as genai

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
# Create the model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro", generation_config=generation_config
)


def clean_and_structure_content(content, page_properties):
    # Convert page_properties to a formatted string
    properties_str = json.dumps(page_properties, indent=2)

    prompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are a skilled social media manager specializing in educational content. Your task is to optimize scholarship summaries from Notion for engaging Facebook posts that attract potential applicants.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. Review the provided scholarship information.
    2. Identify the key details that would be most appealing to potential applicants.
    3. Craft a concise, engaging summary that highlights these key points.
    4. Format the summary for easy readability on Facebook.
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: Use emojis sparingly to highlight key points.
    2. Do: Include a clear call-to-action with the application deadline.
    3. Don’t: Exceed 280 characters (including spaces) to ensure the post is not cut off.
    4. Don’t: Use jargon or complex terms that might confuse potential applicants.
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    The scholarship information is extracted from a Notion database and includes details such as the major or course, eligibility criteria, benefits, and application deadline.
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. Use emojis at the start of each key point.
    2. Start with an attention-grabbing phrase.
    3. List key details in bullet points.
    4. End with the application deadline.
    5. DO NOT ADD HYPERLINK AS THIS IS ALREADY HARDCODED.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your responses:
    1. Example #1
        Input:
        {{
        "For which major or course?": ["Computer Science", "Artificial Intelligence"],
        "Who can apply?": "Female undergraduates",
        "What do I get?": ["$10,000 scholarship", "Tuition coverage", "Monthly allowance", "Internship opportunity"],
        "Until when can I apply?": "2024-12-01"
        }}
        Thoughts: This scholarship is specifically for women in tech, focusing on AI. The financial benefits are comprehensive, and there's a career opportunity included. The deadline is quite far in the future, which is good to mention.
        Output: 🌟 Calling all women in tech! The XYZ Scholarship awards $10,000 for undergraduates in Computer Science with an AI focus. Comprehensive financial aid, including tuition and allowances, plus career opportunities with Megaworld.
    🗓 Apply by: December 1, 2024
    🎯 Eligibility: 85% GPA in SHS or university.
    💼 Benefits: $10,000 scholarship, Tuition coverage, Monthly allowance, Internship opportunity.

    2. Example #2
        Input:
        {{
        "For which major or course?": ["Engineering", "Mathematics", "Physics"],
        "Who can apply?": "High school seniors",
        "What do I get?": ["Full tuition coverage", "Mentorship program"],
        "Until when can I apply?": "2024-03-15"
        }}
        Thoughts: This scholarship targets STEM fields and is for high school seniors. The full tuition coverage is a major benefit, and the mentorship program adds value. The deadline is closer than the previous example.
        Output: 🚀 Future STEM leaders, listen up! Full tuition scholarship for high school seniors in Engineering, Math, or Physics. Plus, get paired with an industry mentor to kickstart your career.
    🗓 Apply by: March 15, 2024
    🎯 For: High school seniors with a passion for STEM.
    💼 Benefits: Full tuition coverage, Mentorship program.
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. Keep the summary concise and engaging, highlighting the most appealing aspects of the scholarship.
    2. Always include the application deadline and eligibility criteria.
    3. Use a consistent format with emojis to make the post visually appealing and easy to read.
    4. DO NOT include a hyperlink section. I have already hardcoded such.
    </RECAP>

    Now, it's your turn to craft an engaging Facebook post for the scholarship information provided below:
    {content} {properties_str}
    """

    try:
        response = model.generate_content(prompt)
        structured_content = response.text.strip()
        return structured_content
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return content
