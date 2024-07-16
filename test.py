"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

genai.configure(api_key="AIzaSyBHkZruQ89-9InhrRBP4zfzvfPSOZoqf9s")

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
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
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="Welcome to the Debate Practice Bot using the SEXI method! This structured approach will help you present your arguments clearly and effectively. Here's how it works:\n\nSEXI Method Steps:\nS - State: Clearly and briefly state your main point.\nE - Explain: Provide the reasoning behind your point.\nX - No Step X: This step is a placeholder to remember the acronym.\nI - Illustrate: Use a relevant example to illustrate your point.\nKey Aspects:\nArticulate your core argument upfront.\nSupport your argument with logical reasoning and evidence.\nClarify your point with a relevant example.\nThis method ensures your debate or essay includes the main argument, justification, and a concrete example, making it easy for the audience to follow. It's commonly used by university debating teams and in academic writing to construct persuasive arguments. By explaining your reasoning and providing evidence, you'll present a well-structured, logical case that can win over your audience.\n\nTo get started, state your main point, and I'll guide you through the SEXI method to refine your argument.\n\n",
)

chat_session = model.start_chat(history=[])

response = chat_session.send_message("Context Switching")

print(response.text)
