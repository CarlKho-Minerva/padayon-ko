import numpy as np
import google.generativeai as genai
from datetime import datetime, timedelta
from cache_utils import load_cache, save_cache
from config import CACHE_EXPIRY_DAYS


def embed_content(title, text, model="models/embedding-001"):
    print(f"Embedding content with title: {title}")
    embedding = genai.embed_content(
        model=model, content=text, task_type="retrieval_document", title=title
    )["embedding"]
    return embedding


def find_best_matches(query, summaries, top_n=3, model="models/embedding-001"):
    print(f"Finding best matches for query.")
    query_embedding = genai.embed_content(
        model=model, content=query, task_type="retrieval_query"
    )["embedding"]

    cache = load_cache()
    embedded_summaries = []
    for summary in summaries:
        cache_key = f"{summary['title']}_{summary['summary']}"
        if cache_key in cache and (
            datetime.now() - datetime.fromisoformat(cache[cache_key]["timestamp"])
        ) < timedelta(days=CACHE_EXPIRY_DAYS):
            embedded_summary = cache[cache_key]["embedding"]
        else:
            embedded_summary = embed_content(summary["title"], summary["summary"])
            cache[cache_key] = {
                "embedding": embedded_summary,
                "timestamp": datetime.now().isoformat(),
            }
        embedded_summaries.append(embedded_summary)

    save_cache(cache)

    query_embedding_array = np.array(query_embedding)
    embedded_summaries_array = np.array(embedded_summaries)

    print(f"Query embedding shape: {query_embedding_array.shape}")
    print(f"Embedded summaries shape: {embedded_summaries_array.shape}")

    if query_embedding_array.shape[0] != embedded_summaries_array.shape[1]:
        raise ValueError("Mismatch in dimensions between query and summary embeddings.")

    dot_products = np.dot(embedded_summaries_array, query_embedding_array)
    indices = np.argsort(dot_products)[-top_n:][::-1]
    print(f"Best match indices: {indices}")

    return indices
