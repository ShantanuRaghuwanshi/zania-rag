from config import OPENAI_API_KEY
import numpy as np
import faiss
import logging
from openai import OpenAI

api_key = OPENAI_API_KEY
client = OpenAI(api_key=api_key)


def get_openai_embedding(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def retrieve_relevant_chunks(query, index, chunks, top_k=5):
    # Set up logging configuration
    logging.basicConfig(filename="retrieve_chunks.log", level=logging.INFO)

    # Add logging statements
    logging.info("Starting retrieve_relevant_chunks function")

    query_vector = np.array(get_openai_embedding(query), dtype=np.float32).reshape(
        1, -1
    )
    logging.debug("Query vector: %s", query_vector)

    distances, indices = index.search(query_vector, top_k)
    logging.debug("Distances: %s", distances)
    logging.debug("Indices: %s", indices)

    relevant_chunks = [chunks[i] for i in indices[0]]
    logging.info("Relevant chunks: %s", relevant_chunks)

    logging.info("Finished retrieve_relevant_chunks function")

    return relevant_chunks
