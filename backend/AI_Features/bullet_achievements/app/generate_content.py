from utils import model


def generate_bullet_point(structuredAchievement):
    bulletPrompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are a career development coach. Your task is to create concise, impactful bullet point summaries of achievements for resumes using the X-Y-Z formula.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. Review the structured achievement details provided.
    2. Start the bullet point with a strong action verb.
    3. Include quantifiable results to highlight the achievement's impact.
    4. Hint at the broader significance of the achievement.
    5. Ensure the bullet point is concise and impactful.
    </INSTRUCTIONS>



    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: Use clear and precise language.
    2. Do: Ensure the bullet point is action-oriented and result-driven.
    3. Don’t: Include unnecessary details or filler words.
    4. Don’t: Use jargon that may confuse the reader.
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    The individual structured their achievement using the X-Y-Z formula. They need a bullet point that captures the essence of their accomplishment in a resume-friendly format.
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. Start with a strong action verb.
    2. Include quantifiable results.
    3. Hint at the broader significance.
    4. Ensure the bullet point is concise and impactful.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your responses:
    1. Example #1
        - **Input**:
            - X (Accomplishment): Founded and grew a successful coding club
            - Y (Measurement): Attracted 30 members and organized a school-wide hackathon
            - Z (Method): Leveraged leadership and organizational skills to create engaging coding activities and events
        - **Output**:
            - • Spearheaded school's first coding club, growing membership to 30 students and orchestrating a successful hackathon, fostering a culture of innovation and tech literacy
    2. Example #2
        - **Input**:
            - X (Accomplishment): Led a successful fundraising initiative
            - Y (Measurement): Raised $5,000 for a local charity
            - Z (Method): Utilized leadership and event planning skills to organize community engagement activities
        - **Output**:
            - • Led fundraising initiative, raising $5,000 for local charity through organized community engagement activities, supporting families in need
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. Start with a strong action verb.
    2. Include quantifiable results.
    3. Hint at the broader significance.
    4. Ensure the bullet point is concise and impactful.
    </RECAP>

    Create a concise, impactful bullet point summary of this achievement using the X-Y-Z formula. Start with a strong action verb, include quantifiable results, and hint at broader significance.

    Input:
    {structuredAchievement}

    Output:
    •
    """
    response = model.generate_content(bulletPrompt)
    return response.text


def generate_detailed_description(bulletPoint, structuredAchievement):
    descriptionPrompt = f"""
<OBJECTIVE_AND_PERSONA>
You are an expert writer skilled in crafting detailed descriptions from bullet points. Your task is to expand a given bullet point into a detailed description, incorporating context, actions, impacts, challenges, skills, and relevance.
</OBJECTIVE_AND_PERSONA>

<INSTRUCTIONS>
To complete the task, follow these steps:
1. Provide context and importance of the achievement.
2. Describe specific actions taken and leadership demonstrated.
3. Include quantifiable impacts and results.
4. Mention challenges overcome.
5. Highlight skills developed or applied.
6. Explain relevance to future goals or field of study.
Ensure the description is under 4 sentences and maintains a natural, non-AI tone.
</INSTRUCTIONS>

<CONSTRAINTS>
Please adhere to the following dos and don'ts:
1. Do: Expand the bullet point accurately and clearly.
2. Do: Maintain a natural, human-like tone.
3. Don’t: Exceed 4 sentences in the description.
</CONSTRAINTS>

<CONTEXT>
Here is the context you need to know:
You are provided with a bullet point and a structured achievement breakdown (accomplishment, measurement, and method) to create a detailed and engaging description.
</CONTEXT>

<OUTPUT_FORMAT>
The output should be formatted as follows:
1. A detailed description under 4 sentences.
2. Maintain a natural, non-AI tone.
</OUTPUT_FORMAT>

<FEW_SHOT_EXAMPLES>
Here is an example to guide your responses:
1. Example #1
    Input:
    Bullet: • Spearheaded school's first coding club, growing membership to 30 students and orchestrating a successful hackathon, fostering a culture of innovation and tech literacy
    Structure:
    X (Accomplishment): Founded and grew a successful coding club
    Y (Measurement): Attracted 30 members and organized a school-wide hackathon
    Z (Method): Leveraged leadership and organizational skills to create engaging coding activities and events
    Output:
    As a passionate coder, I noticed a lack of programming opportunities at my school and took the initiative to start our first-ever coding club. Despite initial skepticism from the administration, I persevered and grew our membership to 30 dedicated students through engaging weekly workshops and coding challenges. The highlight of our first year was organizing a school-wide hackathon, where teams developed innovative solutions to local community problems, showcasing our newly acquired skills and fostering a culture of tech enthusiasm. This experience not only honed my leadership and event planning abilities but also reinforced my commitment to making technology education more accessible to my peers.
</FEW_SHOT_EXAMPLES>

<RECAP>
To summarize, remember the key points:
1. Provide context and importance of the achievement.
2. Describe specific actions and leadership demonstrated.
3. Include quantifiable impacts and results.
4. Mention challenges overcome.
5. Highlight skills developed or applied.
6. Explain relevance to future goals or field of study.
Ensure the description is under 4 sentences and maintains a natural tone.
</RECAP>

Now generate a detailed description for this achievement:
Input:
Bullet: {bulletPoint}
Structure: {structuredAchievement}

Output:
    """
    response = model.generate_content(descriptionPrompt)
    return response.text
