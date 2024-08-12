import os
import tempfile
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier
from flask import Flask, request, jsonify
from pdf_processor.extract_text import extract_text_from_pdf
from pdf_processor.chunk_text import chunk_text
from vector_db.store_chunks import store_chunks_in_vector_db
from vector_db.retrieve_chunks import retrieve_relevant_chunks
from llm.generate_response import generate_response
from config import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET

app = Flask(__name__)
client = WebClient(token=SLACK_BOT_TOKEN)
# signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)


@app.route("/slack/events", methods=["POST"])
def slack_events():
    # if not signature_verifier.is_valid_request(request.get_data(), request.headers):
    #     return "Request verification failed", 400

    event_data = request.json
    if "event" in event_data:
        event = event_data["event"]
        if event["type"] == "message" and "files" in event:
            for file_info in event["files"]:
                if file_info["filetype"] == "pdf":
                    handle_pdf_file(file_info, event["channel"], event["text"])
    return jsonify({"status": "ok"})


def handle_pdf_file(file_info, channel, query):
    try:
        file_id = file_info["id"]
        file_url = file_info["url_private"]
        headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
        response = client.api_call("files.info", params={"file": file_id})
        file_content = client.api_call(
            "files.download", params={"file": file_id}, headers=headers
        )

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content.content)
            temp_file_path = temp_file.name

        text = extract_text_from_pdf(temp_file_path)
        chunks = chunk_text(text)
        index = store_chunks_in_vector_db(chunks)
        relevant_chunks = retrieve_relevant_chunks(query, index, chunks)
        answer = generate_response(relevant_chunks, query)

        client.chat_postMessage(channel=channel, text=answer)
    except SlackApiError as e:
        print(f"Error uploading file: {e.response['error']}")


if __name__ == "__main__":
    app.run(port=3000)
