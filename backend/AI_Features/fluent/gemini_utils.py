import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

conversations = {}


def generate_ai_response(conversation_id, user_input, mode):
    if conversation_id not in conversations:
        conversations[conversation_id] = model.start_chat(history=[])

    chat = conversations[conversation_id]

    prompt = f"""You are an AI communication coach, designed to help users improve their verbal skills in various scenarios. The current mode is: {mode}.

Context: The user is practicing {mode} skills. They have just provided the following input: "{user_input}"

Your task is to:
1. Analyze the user's input based on the guidelines for {mode}.
2. Provide constructive feedback on their communication.
3. Offer suggestions for improvement.
4. Give an example of how the response could be enhanced.
5. Encourage the user to try again with the improvements in mind.

Guidelines for {mode}:

{get_mode_guidelines(mode)}

Please respond in a friendly, encouraging tone. Your response should be structured as follows:
1. Brief analysis of the user's input
2. Positive feedback on what was done well
3. Areas for improvement
4. An example of an enhanced response
5. Encouragement to try again

Remember to tailor your response specifically to the {mode} scenario and the user's input."""

    response = chat.send_message(prompt)
    return response.text


def get_mode_guidelines(mode):
    guidelines = {
        "debate": "Use the SEXI structure: State, Explain, provide an eXample, describe the Impact. Encourage logical arguments, use of evidence, and addressing counterpoints.",
        "storytelling": "Focus on the 5 C's: Characters, Conflict, Choice, Consequences, and Conclusion. Encourage vivid descriptions, emotional engagement, and a clear narrative arc.",
        "qa": "For asking questions: Use OPEN (Open-ended, Probing, Empathetic, Non-judgmental). For answering: Use STAR (Situation, Task, Action, Result). Encourage clarity, relevance, and depth in both questions and answers.",
        "explain": "Use the ELI5 method: Simplify complex ideas, use Analogies, Visualize concepts, and provide Examples. Encourage clear, concise explanations that avoid jargon and relate to familiar concepts.",
    }
    return guidelines.get(mode, "Focus on clear, engaging communication.")
