import os
from dotenv import load_dotenv
import google.generativeai as genai
import markdown

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    tools="code_execution",
)

conversations = {}


def generate_ai_response(conversation_id, user_input, mode):
    if conversation_id not in conversations:
        conversations[conversation_id] = model.start_chat(history=[])

    chat = conversations[conversation_id]

    prompt = f"""
    You are an AI communication partner, engaging in a {mode} conversation. The user has just provided the following input: "{user_input}"

    Your task is to:
    1. Respond naturally to the user's input, continuing the {mode} conversation.
    2. Keep the conversation flowing and engaging.
    3. Encourage the user to elaborate or provide more details if necessary.
    4. Do not repeat or append previous messages. Respond only to the current input.
    5. If the user's input is similar to a previous one, acknowledge it and ask for clarification or new information.

    Remember to tailor your response specifically to the {mode} scenario and the user's current input."""

    response = chat.send_message(prompt)
    return response.text


def generate_feedback(conversation_id, mode):
    if conversation_id not in conversations:
        return "<p>No conversation found to provide feedback on.</p>"

    chat = conversations[conversation_id]
    conversation_history = chat.history

    feedback_prompt = f"""
    You are an AI communication coach, analyzing a completed {mode} conversation. Please review the conversation history and provide feedback to the user practicing their verbal speech based on the following guidelines:

    Guidelines for {mode}:
    {get_mode_guidelines(mode)}

    Your task is to:
    1. Analyze the overall flow and effectiveness of the conversation.
    2. Identify strengths in the user's communication.
    3. Suggest areas for improvement.
    4. Provide specific examples from the conversation to illustrate your points.
    5. Offer actionable advice for future conversations.
    6. One paragraph response only no formatting.

    Please structure your feedback as follows:
    1. Overall assessment
    2. Strengths
    3. Areas for improvement
    4. Specific examples
    5. Actionable advice
    6. One paragraph response only no formatting.

    Remember to be constructive and encouraging in your feedback."""

    feedback_response = model.generate_content(
        feedback_prompt + "\n\nConversation history:\n" + str(conversation_history)
    )

    # Convert Markdown to HTML
    html_feedback = markdown.markdown(feedback_response.text)

    return html_feedback


def get_mode_guidelines(mode):
    guidelines = {
        "debate": "Use the SEXI structure: State, Explain, provide an eXample, describe the Impact. Encourage logical arguments, use of evidence, and addressing counterpoints.",
        "storytelling": "Focus on the 5 C's: Characters, Conflict, Choice, Consequences, and Conclusion. Encourage vivid descriptions, emotional engagement, and a clear narrative arc.",
        "qa": "For asking questions: Use OPEN (Open-ended, Probing, Empathetic, Non-judgmental). For answering: Use STAR (Situation, Task, Action, Result). Encourage clarity, relevance, and depth in both questions and answers.",
        "explain": "Use the ELI5 method: Simplify complex ideas, use Analogies, Visualize concepts, and provide Examples. Encourage clear, concise explanations that avoid jargon and relate to familiar concepts.",
    }
    return guidelines.get(mode, "Focus on clear, engaging communication.")
