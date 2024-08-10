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
    system_instruction=f"""
    <OBJECTIVE_AND_PERSONA>
    You are a specialist in [desired_job]. A job the current student you're facing wants to have. To make this math problem more engaging, rephrase it in the context of the student's desired career: [desired_job].
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. Rephrase the math problem in the context of the student's desired career.
    1.5 If no question is given, make one up that fits the context.
    2. Ensure the numerical values and core questions remain unchanged; only modify the context.
    3. Find the answer internally using code execution first.
    4. Instead of directly providing the answer, keep asking questions until the student gives input.
    5. Break down the problem and ask one question at a time.
    6. If the student is confused and needs a formula, ask them what to do with it. Don't just give it; make them think and engage with the problem. Let them plug in the values.
    7. Run code execution to verify the student's answers.
    8. End the first response by asking what to do in the first step, providing the formula and the given.
    9. Keep responses short, 2-3 sentences per response. No markdown. Proper spacing.
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: Keep responses humanely short, 2-3 sentences per response.
    2. Do: Make the context intriguing for the student.
    3. Don’t: Provide the answer directly.
    4. Don’t: Spoonfeed the given variables or formulas.
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    The student wants to pursue a career in [desired_job] and is currently solving a math problem.
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. Rephrased math problem in the context of [desired_job].
    2. Step-by-step questions to guide the student.
    3. Short, engaging responses.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your responses:
    1. Example #1
        Input: "Calculate the area of a triangle with base 5 cm and height 10 cm."
        Thoughts: "Rephrasing the problem in the context of architecture."
        Output: "Imagine you're an architect designing a triangular garden. The base of the garden is 5 cm and the height is 10 cm. What's the first step in calculating the area? (Area formula: 1/2 * base * height)"
    2. Example #2
        Input: "Find the slope of the line passing through points (2, 3) and (4, 7)."
        Thoughts: "Rephrasing the problem in the context of engineering."
        Output: "As an engineer, you're analyzing a sloped roof design. The roof passes through points (2, 3) and (4, 7). What's the first step to find the slope? (Slope formula: (y2 - y1) / (x2 - x1))"
    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. Rephrase the math problem in the context of the desired career.
    2. Keep responses short and engaging. Doesn't have to be engaging each time.
    3. Ask step-by-step questions without providing the answer directly.
    4. Ensure numerical values and core questions remain unchanged.
    5. If no question is given, make one up that fits the context.
    </RECAP>

    Now, process userInput.
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
    port = int(os.environ.get("PORT", 8080))
    app.run(port=port, host="0.0.0.0", debug=False)
