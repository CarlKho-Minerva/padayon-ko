import numpy as np
import google.generativeai as genai


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


def generate_scholarship_application(essays, achievements, GenAI_model):
    prompt = f"""Based on the following essays and achievements, write a comprehensive scholarship application:

    Essays:
    {' '.join(essays)}

    Achievements:
    {' '.join(achievements)}

    Please create a compelling scholarship application that showcases the applicant's qualifications, experiences, and potential."""

    response = GenAI_model.generate_content(prompt)
    return response.text
