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


def generate_scholarship_application(query, essays, achievements, GenAI_model):
    prompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are an expert in crafting compelling scholarship applications. Your task is to write a comprehensive and persuasive scholarship application based on the query provided, using the provided essays and achievements as supplementary materials.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete this task, follow these steps:
    1. Review the provided query, essays, and achievements.
    2. Develop a cohesive and persuasive scholarship application that aligns with the query.
    3. Highlight the applicant’s qualifications, experiences, and potential by integrating insights from the essays and achievements.
    4. Ensure that the application is well-structured, professional, and engaging.
    </INSTRUCTIONS>

    <CONTEXT>
    Here is the context you need to know:
    - The query provides the specific focus or theme for the scholarship application.
    - The essays and achievements offer detailed information about the applicant’s background, accomplishments, and goals.

    Query:
    {query}

    Essays:
    {' '.join(essays)}

    Achievements:
    {' '.join(achievements)}
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. A persuasive and well-organized scholarship application.
    2. Include an introduction, body paragraphs that highlight the applicant’s qualifications and experiences, and a conclusion.
    3. Maintain clarity, coherence, and relevance to the query and scholarship objectives.
    </OUTPUT_FORMAT>

    <RECAP>
    To summarize, remember the key points:
    1. Address the query with a persuasive and well-structured application.
    2. Integrate information from the essays and achievements effectively.
    3. Ensure the application is professional, clear, and aligned with scholarship goals.
    </RECAP>

    Now, based on the query, essays, and achievements provided, create the scholarship application.
    """

    response = GenAI_model.generate_content(prompt)
    return response.text
