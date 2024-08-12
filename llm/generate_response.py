import logging
from openai import OpenAI
from config import OPENAI_API_KEY

api_key = OPENAI_API_KEY

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO)


def generate_response(relevant_chunks, query):
    client = OpenAI(api_key=OPENAI_API_KEY)
    context = " ".join(relevant_chunks)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Context: {context}\n\nQuestion: {query}\n\nAnswer:",
        },
    ]

    # Log the relevant information
    logging.info(f"Generating response for query: {query}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,
    )

    # Log the generated response
    logging.info(f"Generated response: {response.choices[0].message.content}")

    return response.choices[0].message.content
