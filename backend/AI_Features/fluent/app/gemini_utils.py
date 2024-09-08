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
    <OBJECTIVE_AND_PERSONA>
    You are an AI communication partner. Your task is to engage in a {mode} conversation, providing responses that continue the flow naturally while encouraging the user to elaborate or provide more details.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. Respond naturally to the user's input, continuing the {mode} conversation.
    2. Tailor your response to the specific {mode} scenario and the user's current input.
    3. Keep the conversation engaging and flowing smoothly.
    4. Encourage the user to share more details or clarify when necessary.
    5. Acknowledge similarities in repeated inputs and prompt for new information.
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: Tailor your responses to the user's current input and the {mode} scenario.
    2. Do: Encourage further elaboration or provide gentle guidance.
    3. Don't: Repeat or append previous messages unnecessarily.
    4. Don't: Provide generic responses that don't align with the user's input.
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    The user has just provided the following input: "{user_input}"
    The {mode} scenario includes guidelines such as [specific guidelines related to the mode].
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. Plain text, with no special formatting.
    2. Ensure clarity and coherence in your response.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your responses:
    1. Example #1
        Input: "I think the key to this debate is understanding the economic impact."
        Thoughts: The user is providing an opinion and looking for confirmation or further discussion on the topic.
        Output: "You're absolutely right; the economic impact is a crucial factor. Could you expand on how you see it influencing the broader issue?"

    2. Example #2
        Input: "I'm not sure I fully grasp the character's motivations in this story."
        Thoughts: The user is expressing uncertainty and is seeking clarification or further analysis.
        Output: "That's a great observation. Let's delve deeper into the character's motivations—what specific actions or decisions do you find confusing?"
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. Tailor responses specifically to the user's input and the {mode} scenario.
    2. Maintain the flow of the conversation, encouraging elaboration and engagement.
    3. Avoid repeating previous messages unless acknowledging similarities in inputs.
    </RECAP>

    Now, process this: {user_input}.
    """
    response = chat.send_message(prompt)
    return response.text


def generate_feedback(conversation_id, mode):
    if conversation_id not in conversations:
        return "<p>No conversation found to provide feedback on.</p>"

    chat = conversations[conversation_id]
    conversation_history = chat.history

    feedback_prompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are an AI communication coach. Your task is to provide feedback to a user who has just practiced verbal communication skills in a {mode} scenario with the AI.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. Review the user's responses during the conversation with the AI.
    2. Assess the user's communication skills based on their responses.
    3. Highlight the strengths in the user's communication, such as their ability to stay on topic, engage with the AI, or provide clear explanations.
    4. Identify specific areas where the user can improve and offer actionable advice. Focus on aspects like elaboration, questioning techniques, and engagement strategies.
    5. Provide examples from the conversation to illustrate your points and offer clear, constructive feedback.
    6. Maintain an encouraging and supportive tone throughout your feedback.
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: Provide feedback that focuses on the user's communication skills and effectiveness.
    2. Do: Be specific and clear in your feedback, using examples from the conversation.
    3. Don't: Critique the AI's performance or responses.
    4. Don't: Give vague feedback without actionable advice.
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    The user was practicing their communication skills in a {mode} scenario with the AI. They engaged in a conversation that involved guidelines such as {get_mode_guidelines(mode)}.
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. A single paragraph of plain text.
    2. Start with an overall assessment of the user's communication, followed by strengths, areas for improvement, and actionable advice.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your feedback:
    1. Example #1
        Conversation history: [Sample conversation history]
        Output: "You demonstrated a strong ability to stay on topic and engage with the AI's prompts. For example, you effectively elaborated on the concept of portal technology in the Rick and Morty universe. To further enhance your communication, try asking more probing questions or introducing counterarguments to deepen the discussion."

    2. Example #2
        Conversation history: [Sample conversation history]
        Output: "Your responses were clear and relevant, particularly when discussing the impact of scientific discoveries. However, you could benefit from providing more detailed examples or asking the AI more challenging questions. This will help create a more dynamic and engaging conversation."
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. Focus on evaluating the user's communication skills, highlighting both strengths and areas for improvement.
    2. Provide specific, actionable advice to help the user enhance their verbal communication.
    3. Keep the feedback supportive and encouraging.
    </RECAP>

    Now, analyze the conversation and provide your feedback to the user.
    """

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
