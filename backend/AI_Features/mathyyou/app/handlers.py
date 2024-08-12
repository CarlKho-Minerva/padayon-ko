from flask import jsonify
from chat import create_chat_session, get_chat_session, chat_sessions


def handle_initial_questions():
    print("[DEBUG\n\n] Handling initial questions\n\n")
    questions = [
        "Hi. I'm MathyYou. I align boring math questions to your interest. Can you tell me what you're interested in?",
        "What is the math problem? If you don't have one, we will give you a sample. Just type 'skip'",
        "What kind of math do you want to practice solving? College-level or everyday math?",
    ]
    print("[DEBUG\n\n] Returning questions:", questions, "\n\n")
    return jsonify({"questions": questions})


def handle_start_chat(data, model):
    print("[DEBUG\n\n] Handling start chat with data:", data, "\n\n")
    interest = data.get("interest")
    problem = data.get("problem")
    level = data.get("level")

    chat_id = create_chat_session(model)
    print("[DEBUG\n\n] Created chat session with ID:", chat_id, "\n\n")

    chat_session = chat_sessions[chat_id]["session"]

    if problem != "skip":
        prompt = f"I'm interested in {interest}. The math I have to solve is: {problem}. Keep in mind my proficiency level or the type I want to practice on is {level} mathematics."
    else:
        prompt = f"I'm interested in {interest}. Please create a simple sample math problem. Note that my proficiency level or the type I want to practice on is {level} mathematics."

    print("[DEBUG\n\n] Sending prompt to chat session:", prompt, "\n\n")
    response = chat_session.send_message(prompt)
    chat_sessions[chat_id]["history"].append({"role": "user", "content": prompt})
    chat_sessions[chat_id]["history"].append({"role": "ai", "content": response.text})

    print("[DEBUG\n\n] Chat session response:", response.text, "\n\n")
    return jsonify({"response": response.text, "chat_id": chat_id})


def handle_chat(data):
    print("[DEBUG\n\n] Handling chat with data:", data, "\n\n")
    user_input = data.get("message")
    chat_id = data.get("chat_id")

    chat_session_data = get_chat_session(chat_id)
    if not chat_session_data:
        print("[DEBUG\n\n] Invalid chat session\n\n")
        return jsonify({"error": "Invalid chat session"}), 400

    chat_session = chat_session_data["session"]
    history = chat_session_data["history"]

    history.append({"role": "user", "content": user_input})
    prompt = "\n".join([f"{entry['role']}: {entry['content']}" for entry in history])
    print("[DEBUG\n\n] Sending prompt to chat session:", prompt, "\n\n")
    response = chat_session.send_message(prompt)
    history.append({"role": "ai", "content": response.text})

    print("[DEBUG\n\n] Chat session response:", response.text, "\n\n")
    return jsonify({"response": response.text})
