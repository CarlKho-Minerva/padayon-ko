from utils import model


def extract_key_info(cleanedInput):
    extractPrompt = f"""
<OBJECTIVE_AND_PERSONA>
You are an expert in identifying and summarizing key information from textual descriptions. Your task is to extract and clearly present key achievements and details from the provided input.
</OBJECTIVE_AND_PERSONA>

<INSTRUCTIONS>
To complete the task, follow these steps:
1. Identify and extract specific roles and responsibilities mentioned in the input.
2. Highlight quantifiable results such as numbers, percentages, etc.
3. Note the impact on the community or organization.
4. Outline the skills developed or demonstrated.
5. Mention any challenges overcome.
6. Provide the time frame and context of the achievement.
</INSTRUCTIONS>

<CONSTRAINTS>
Please adhere to the following dos and don'ts:
1. Do: Extract and present information concisely and accurately.
2. Do: Maintain the original meaning and context of the input.
3. Don’t: Add any new information not present in the original input.
</CONSTRAINTS>

<CONTEXT>
Here is the context you need to know:
The task involves extracting key achievements and details from user-provided input, focusing on roles, results, impact, skills, challenges, and time frame.
</CONTEXT>

<OUTPUT_FORMAT>
The output should be formatted as follows:
1. Role: [specific role]
2. Time frame: [time frame]
3. Quantifiable result: [result]
4. Achievement: [achievement]
5. Skills: [skills]
6. Impact: [impact]
7. Challenges: [challenges]
</OUTPUT_FORMAT>

<FEW_SHOT_EXAMPLES>
Here are some examples to guide your responses:
1. Example #1
    Input: "I started a coding club at my school last year. We managed to get about 30 members and organized a hackathon."
    Output:
    - Role: Founder of coding club
    - Time frame: Last year
    - Quantifiable result: 30 members
    - Achievement: Organized a hackathon
    - Skills: Leadership, organization, coding
    - Impact: Increased coding interest in school
2. Example #2
    Input: "Led a team to develop a mobile app that was downloaded 10,000 times in the first month."
    Output:
    - Role: Team leader
    - Time frame: First month
    - Quantifiable result: 10,000 downloads
    - Achievement: Developed a mobile app
    - Skills: Team management, app development
    - Impact: Successful product launch
    - Challenges: Coordinating team efforts
</FEW_SHOT_EXAMPLES>

<RECAP>
To summarize, remember the key points:
1. Extract and present specific roles and responsibilities.
2. Highlight quantifiable results and their impact.
3. Note the skills developed or demonstrated.
4. Mention challenges overcome.
5. Provide the time frame and context of the achievement.
</RECAP>

Now extract key information from this input:
Input: "{cleanedInput}"

Output:
    """
    response = model.generate_content(extractPrompt)
    return response.text
