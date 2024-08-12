import faiss
import numpy as np
from config import OPENAI_API_KEY
from config import OPENAI_API_KEY
from openai import OpenAI

api_key = OPENAI_API_KEY
client = OpenAI(api_key=api_key)


def get_openai_embedding(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def store_chunks_in_vector_db(chunks):
    embeddings = [get_openai_embedding(chunk) for chunk in chunks]
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))
    return index
