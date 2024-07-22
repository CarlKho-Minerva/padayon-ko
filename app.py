from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
    Rewrite the given essay according to best practices. Make it clear, concise, and impactful.
    """,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rewrite', methods=['POST'])
def rewrite():
    try:
        data = request.get_json()
        if not data or 'essay' not in data:
            return jsonify({'error': 'Invalid input'}), 400

        essay = data['essay']
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(essay)
        return jsonify({'rewritten_essay': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)