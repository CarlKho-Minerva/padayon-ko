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

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    tools="code_execution",
)


def functionnamehere(userInput):
    prompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are a [insert persona, such as "math tutor" or "coding expert"]. Your task is to [insert objective, such as "help students solve math problems without giving the answers directly"].
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. [First step]
    2. [Second step]
    3. ...
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: [First do]
    2. Do: [Second do]
    3. Don’t: [First don't]
    4. Don’t: [Second don't]
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    [Provide relevant background information, documents, or data here]
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. [Specify desired format, e.g., Markdown, JSON, table]
    2. ...
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your responses:
    1. Example #1
        Input: [Input example]
        Thoughts: [Model's reasoning process]
        Output: [Expected output]
    2. Example #2
        Input: [Input example]
        Thoughts: [Model's reasoning process]
        Output: [Expected output]
    ...
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. [Reiterate the constraints]
    2. [Reiterate the output format]
    3. [Any other crucial instructions]
    </RECAP>

    Now, process this: {userInput}.
    """

    response = model.generate_content(prompt)
    return response.text
