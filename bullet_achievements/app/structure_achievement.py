from utils import model


def structure_achievement(extractedInfo):
    # Define the prompt for structuring the achievement using the X-Y-Z formula
    structurePrompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are a skilled achievement evaluator. Your task is to structure the provided achievement using the X-Y-Z formula: "Accomplished [X] as measured by [Y], by doing [Z]". Your goal is to present a comprehensive yet concise structure of the achievement.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. Identify and clearly state the accomplishment (X).
    2. Quantify the measurement of the accomplishment (Y).
    3. Describe the method or actions taken to achieve the accomplishment (Z).
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: Ensure that each component (X, Y, Z) is clearly defined and specific.
    2. Do: Provide a concise and accurate summary.
    3. Don’t: Use vague or ambiguous terms.
    4. Don’t: Include unnecessary details or embellishments.
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    - The X-Y-Z formula helps structure achievements to clearly highlight the accomplishment, the measurement of success, and the method used.
    - Ensure the output is structured according to the given formula while being easy to understand.
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. X (Accomplishment): [Clearly state the accomplishment]
    2. Y (Measurement): [Quantify the result]
    3. Z (Method): [Describe the actions or methods used]
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your responses:
    1. Example #1
        Input:
        - Role: Led a fundraising campaign
        - Time frame: Six months
        - Quantifiable result: Raised $10,000
        - Achievement: Successfully funded a community project
        - Skills: Leadership, fundraising
        - Impact: Enabled the completion of a community center
        Output:
        X (Accomplishment): Led a successful fundraising campaign
        Y (Measurement): Raised $10,000
        Z (Method): Utilized leadership and organizational skills to plan and execute fundraising events
    2. Example #2
        Input:
        - Role: Organized a tech workshop
        - Time frame: One month
        - Quantifiable result: 50 participants
        - Achievement: Improved tech skills among local youth
        - Skills: Event planning, technical training
        - Impact: Enhanced tech proficiency in the community
        Output:
        X (Accomplishment): Organized a tech workshop
        Y (Measurement): Engaged 50 participants
        Z (Method): Planned and executed the workshop with a focus on interactive and practical learning
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. Clearly define each component of the X-Y-Z formula.
    2. Ensure the output is concise and specific.
    3. Avoid vague terms and unnecessary details.
    </RECAP>

    Input: {extractedInfo}

    Output:
    X (Accomplishment):
    Y (Measurement):
    Z (Method):
    """

    # Call the Gemini API or model to generate a response based on the structurePrompt
    response = model.generate_content(structurePrompt)
    structured_text = response.text.strip()
    return structured_text
