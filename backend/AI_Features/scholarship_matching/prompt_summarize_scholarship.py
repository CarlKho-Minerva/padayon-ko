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


def summarize_scholarship(scholarship_data):
    prompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are a professional summarizer specializing in creating concise, relevant, and clear summaries of scholarship opportunities for students.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    You will be provided with a full description of a scholarship. Your task is to generate a concise summary that captures the essential details of the scholarship, making it easy for students to determine its relevance to their profile.
    1. Extract the following key details from the scholarship description:
        - Name of the scholarship
        - Purpose or focus of the scholarship (e.g., supporting underrepresented students in STEM, promoting innovation in AI)
        - Eligibility criteria (e.g., specific countries, academic levels, fields of study)
        - Preferred fields of study or career paths (e.g., Computer Science, AI, Robotics)
        - Notable requirements (e.g., specific achievements, projects, or interests)
        - Application deadline
        - Award amount or benefits
    2. Combine these details into a summary that is between 50 and 100 words.
    3. Ensure the summary is clear, concise, and highlights the most important aspects of the scholarship for easy matching with student profiles.
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following:
    1. Do: Focus on relevant information that will help students understand the scholarship's purpose and eligibility.
    2. Do: Use clear and straightforward language.
    3. Don't: Include unnecessary details or overly technical language that might confuse the reader.
    4. Don't: Omit critical details like eligibility or application deadlines.
    </CONSTRAINTS>

    <OUTPUT_FORMAT>
    Output a single string containing the summarized scholarship information.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples:
    1. Example #1
        Input: "The XYZ Scholarship aims to support women in technology pursuing degrees in Computer Science. Open to undergraduate students worldwide, the scholarship provides $10,000 for tuition. Applicants must demonstrate academic excellence and have a strong interest in AI research. Deadline: December 1st."
        Output: "XYZ Scholarship supports women in tech, offering $10,000 for Computer Science undergraduates with an interest in AI. Open globally; deadline: December 1st."

    2. Example #2
        Input: "The ABC Innovation Grant encourages creative solutions in sustainable agriculture. Open to graduate students in Environmental Science, the grant awards $5,000 for research projects focused on smart farming. Applicants must submit a project proposal and demonstrate prior experience in sustainable practices. Deadline: March 15th."
        Output: "ABC Innovation Grant offers $5,000 for graduate research in sustainable agriculture, focusing on smart farming. Open to Environmental Science students; deadline: March 15th."

    3. Example #3
        Input: "The DEF Scholarship supports underrepresented minorities in STEM. Available to high school seniors planning to major in any STEM field, this scholarship offers $2,500 towards tuition. Applicants must have a minimum GPA of 3.5 and demonstrate leadership in community service. Deadline: May 1st."
        Output: "DEF Scholarship offers $2,500 for underrepresented minorities in STEM. Open to high school seniors with a 3.5 GPA and leadership in community service; deadline: May 1st."

    <RECAP>
    Generate a clear, concise scholarship summary using the provided information, focusing on the most important details for student matching.
    </RECAP>

    Now, generate a summary using this scholarship information: {scholarship_data}
    """
    response = model.generate_content(prompt)
    return response.text
