import os
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai

# Clear any existing environment variable
os.environ.pop("GEMINI_API_KEY", None)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key="gemini_api_key")


def embed_content(title, text, model="models/embedding-001"):
    return genai.embed_content(
        model=model, content=text, task_type="retrieval_document", title=title
    )["embedding"]


def find_best_passages(query, dataframe, top_n=3, model="models/embedding-001"):
    query_embedding = genai.embed_content(
        model=model, content=query, task_type="retrieval_query"
    )["embedding"]
    dot_products = np.dot(np.stack(dataframe["Embeddings"]), query_embedding)
    indices = np.argsort(dot_products)[-top_n:][::-1]
    return dataframe.iloc[indices]
