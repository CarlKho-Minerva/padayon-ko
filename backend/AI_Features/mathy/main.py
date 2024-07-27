# app.py

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)

# Configure the Gemini API (replace with your actual API key)
genai.configure(api_key="")

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-pro")

# Initialize chat history
chat_history = []


def process_message(message, agent):
    global chat_history

    # Debug print
    print(f"Agent: {agent}")
    print(f"Input: {message}")

    # Add user message to chat history
    chat_history.append({"role": "user", "parts": message})

    # Generate prompt based on agent
    if agent == "greeter":
        prompt = f"You are a friendly math tutor. Greet the user and ask about their interests: {message}"
    elif agent == "interpreter":
        prompt = (
            f"Interpret this math question and identify the core concept: {message}"
        )
    elif agent == "scenario_generator":
        prompt = f"Create a real-life scenario based on this math concept and the user's interests: {message}"
    elif agent == "socratic_guide":
        prompt = f"Ask a guiding question to help the user understand this concept: {message}"
    elif agent == "answer_verifier":
        prompt = f"Verify if this answer is correct (use Python internally if needed): {message}"
    else:  # conclusion_agent
        prompt = f"Summarize the learning experience and reinforce the real-life application: {message}"

    # Generate response
    response = model.generate_content(prompt)

    # Add model response to chat history
    chat_history.append({"role": "model", "parts": response.text})

    # Debug print
    print(f"Output: {response.text}")

    return response.text


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]
    agent = request.json["agent"]
    response = process_message(message, agent)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(port=5000, debug=False)
