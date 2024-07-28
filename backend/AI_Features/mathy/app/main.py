from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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
    system_instruction="""
        Imagine you're a specialist in [Future desired job / industry post-grad here]. A job the current student you're facing wants to have. To make this math problem more engaging, rephrase it in the context of the student's desired career: [Future desired job/industry post-grad here].

        Ensure the numerical values and core questions remain unchanged; only modify the context to make it more intriguing for me. Find the answer internally using Code Execution first. Instead of directly providing the answer, keep asking me questions until I give you my input. A call and response scenario.

        Do it in a step-by-step manner. Really breakdown the problem and ask one question at a time instead of giving me the whole formula or spoonfeeding me the given variables.

        If I'm confused and you need to provide a formula, make sure to ask me what to do with it. Don't just give it to me. Make me think and engage with the problem. Let me do the plugging of values.

        Just make sure to run code execution to verify my answers.

        End your first response by starting with asking me what to do in the first step and providing the formula and the given.

        Keep responses humanely short. 2-3 sentences per response. No markdown. Proper spacing.
        """,
    tools="code_execution",
)

chat_sessions = {}


@app.route("/initial_questions", methods=["GET"])
def initial_questions():
    questions = [
        "What are you interested in?",
        "What is the math problem? If you don't have one, we will give you a sample. Just type 'skip'",
        "What kind of math do you want to practice solving? College-level or everyday math?",
    ]
    return jsonify({"questions": questions})


@app.route("/start_chat", methods=["POST"])
def start_chat():
    data = request.json
    interest = data.get("interest")
    problem = data.get("problem")
    level = data.get("level")

    chat_session = model.start_chat(history=[])
    chat_id = id(chat_session)
    chat_sessions[chat_id] = {"session": chat_session, "history": []}

    if problem != "skip":
        prompt = f"I'm interested in {interest}. The math I have to solve is: {problem}. Keep in mind my proficiency level or the type I want to practice on is {level} mathematics."
    else:
        prompt = f"I'm interested in {interest}. Please create a simple sample math problem. Note that my proficiency level or the type I want to practice on is {level} mathematics."

    response = chat_session.send_message(prompt)
    chat_sessions[chat_id]["history"].append({"role": "user", "content": prompt})
    chat_sessions[chat_id]["history"].append({"role": "ai", "content": response.text})

    return jsonify({"response": response.text, "chat_id": chat_id})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    chat_id = data.get("chat_id")

    if chat_id not in chat_sessions:
        return jsonify({"error": "Invalid chat session"}), 400

    chat_session = chat_sessions[chat_id]["session"]
    history = chat_sessions[chat_id]["history"]

    history.append({"role": "user", "content": user_input})
    prompt = "\n".join([f"{entry['role']}: {entry['content']}" for entry in history])
    response = chat_session.send_message(prompt)
    history.append({"role": "ai", "content": response.text})

    return jsonify({"response": response.text})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
