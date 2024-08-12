from pdf_processor.extract_text import extract_text_from_pdf
from pdf_processor.chunk_text import chunk_text
from vector_db.store_chunks import store_chunks_in_vector_db
from vector_db.retrieve_chunks import retrieve_relevant_chunks
from llm.generate_response import generate_response
from slack_integration.slack_bot import app


def main(pdf_path, query):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    index = store_chunks_in_vector_db(chunks)
    relevant_chunks = retrieve_relevant_chunks(query, index, chunks)
    answer = generate_response(relevant_chunks, query)
    return answer


if __name__ == "__main__":
    # pdf_path = "C:/Users/shant/Downloads/handbook.pdf"
    # msg = ""
    # while True:
    #     query = input("Enter your question (or 'q' to quit): ")
    #     if query == "q":
    #         break
    #     if msg:
    #         query_1 = msg + query
    #     answer = main(pdf_path, query_1)
    #     msg = "query:" + query + "\nanswer:" + answer + "\n"
    #     print(answer)
    app.run(port=3000)
