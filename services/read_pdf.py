import PyPDF2
import openai
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize OpenAI API
openai.api_key = "your_openai_api_key"


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
    return text


# Function to chunk text
def chunk_text(text, chunk_size=1000):
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]
    return chunks


# Function to store chunks in vector database
def store_chunks_in_vector_db(chunks):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks).toarray()
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors, dtype=np.float32))
    return index, vectorizer


# Function to retrieve relevant chunks
def retrieve_relevant_chunks(query, index, vectorizer, chunks, top_k=5):
    query_vector = vectorizer.transform([query]).toarray().astype(np.float32)
    distances, indices = index.search(query_vector, top_k)
    relevant_chunks = [chunks[i] for i in indices[0]]
    return relevant_chunks


# Function to generate response using GPT-4
def generate_response(relevant_chunks, query):
    context = " ".join(relevant_chunks)
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=150
    )
    return response.choices[0].text.strip()


# Main function
def main(pdf_path, query):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    index, vectorizer = store_chunks_in_vector_db(chunks)
    relevant_chunks = retrieve_relevant_chunks(query, index, vectorizer, chunks)
    answer = generate_response(relevant_chunks, query)
    return answer


# Example usage
if __name__ == "__main__":
    pdf_path = "path_to_your_pdf_file.pdf"
    query = "Your query here"
    answer = main(pdf_path, query)
    print(answer)
