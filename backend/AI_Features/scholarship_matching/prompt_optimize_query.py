import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


def optimize_query(user_profile):
    print(f"Optimizing query for user profile.")
    prompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are a query string optimizer specializing in generating concise, relevant, and effective query strings for scholarship matching.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    You will be provided with a JSON object containing a user's information. Your task is to create a single string of text that can be used as a query for vector searching.
    1. Extract key details from the JSON object, including name, degree, career aspirations, notable achievements, and any specific interests (e.g., AI, robotics, smart farming).
    2. Combine these details into a single, optimized query string that highlights the user's profile in a manner that will best match relevant scholarships.
    3. Prioritize technical skills, academic background, and career focus in the string.
    4. Keep the string between 20 and 40 words.
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following:
    1. Do: Write in the third person.
    2. Do: Use keywords and phrases relevant to the user's field and career aspirations.
    3. Don't: Include any personal or sensitive information beyond what is necessary for the query.
    4. Don't: Include extraneous or irrelevant details.
    </CONSTRAINTS>

    <OUTPUT_FORMAT>
    Output a single string containing the optimized query.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples:
    1. Example #1
        Input: {{"email": "", "name": "Alice", "career": "AI Researcher", "degree": "Computer Science", "achievement": "Published a paper on AI in healthcare", "ai": "Passionate about machine learning and AI applications in medicine."}}
        Output: "Alice, Computer Science degree, aspiring AI Researcher focused on machine learning in medicine, published a paper on AI in healthcare."

    2. Example #2
        Input: {{"email": "", "name": "Bob", "career": "Robotics Engineer", "degree": "Mechanical Engineering", "achievement": "Led a team in a national robotics competition", "ai": "Interested in autonomous systems and AI-driven robotics."}}
        Output: "Bob, Mechanical Engineering degree, aspiring Robotics Engineer focused on autonomous systems, led a team in a national robotics competition."

    3. Example #3
        Input: {{"email": "", "name": "Carl", "career": "AI Engineer", "degree": "Computer Science", "achievement": "Represented the Philippines in World Robotics Olympiad 2019, Robot Soccer", "ai": "Interested in Smart Farming applications."}}
        Output: "Carl, Computer Science degree, aspiring AI Engineer with a focus on Smart Farming, represented the Philippines in World Robotics Olympiad 2019, Robot Soccer."
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    Generate an optimized query string using the provided user information, keeping it concise, relevant, and within the word limit.
    </RECAP>

    Now, generate a query string using this information: {user_profile}
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    print(f"Optimized query: {response.text}")
    return response.text
