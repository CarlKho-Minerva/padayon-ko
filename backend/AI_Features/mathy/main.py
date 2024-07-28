"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="""
        Imagine you're a specialist in [Future desired job / industry post-grad here]. A job the current student you're facing wants to have. To make this math problem more engaging, rephrase it in the context of the student's desired career: [Future desired job/industry post-grad here].

        Ensure the numerical values and core questions remain unchanged; only modify the context to make it more intriguing for me. Find the answer internally using Code Execution first. Instead of directly providing the answer, keep asking me questions until I give you my input. A call and response scenario.

        Do it in a step-by-step manner. Really breakdown the proble and ask one question at a time instead of giving me the whole formula or spoonfeeding me the given variables.

        If I'm confused and you need to provide a formula, make sure to ask me what to do with it. Don't just give it to me. Make me think and engage with the problem. Let me do the plugging of values.

        Just make sure to run code execution to verify my answers.

        End your first response by starting with asking me what to do in the first step and providing the formula and the given.

        Keep responses humanely short. 2-3 sentences per response.
        """,
    tools="code_execution",
)

chat_session = model.start_chat(history=[])

interest = input("What are you interested in? ")
problem = input(
    "What is the math problem? If you don't have one, we will give you a sample. Just type 'skip' "
)
level = input(
    "What is kind of math do you want to practice solving? College-level or everyday math? "
)


if problem != "skip":
    prompt_hasProblem = f"I'm interested in {interest}. The math I have to solve is: {problem}. Keep in mind my proficiency level or the type I want to practice on is {level} mathematics."
    response = chat_session.send_message(prompt_hasProblem)

prompt_noProblem = f"I'm interested in {interest}. Please create a simple sample math problem. Note that my proficiency level or the type I want to practice on is {level} mathematics."
response = chat_session.send_message(prompt_noProblem)

print(response.text)

while True:
    user_input = input("You: ")
    response = chat_session.send_message(user_input)
    print(f"AI: {response.text}")
    if "Goodbye" in response.text:
        break
