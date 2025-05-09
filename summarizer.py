import os
import time
import json
from huggingface_hub import InferenceClient
from PyPDF2 import PdfReader

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

# Initialize Hugging Face client
client = InferenceClient(token=hf_token)

def summarize_with_retry(text, retries=5, delay=5):
    for attempt in range(retries):
        try:
            # Use summarization model (facebook/bart-large-cnn)
            summary_response = client.summarization(text=text, model="facebook/bart-large-cnn")
            return summary_response.get('summary_text', '')
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                return f"Error generating summary after {retries} attempts: {e}"

def summarize_pdf(pdf_path):
    # Step 1: Extract text from the PDF
    reader = PdfReader(pdf_path)
    text = ""
    summary_data_list = []
    for page_num, page in enumerate(reader.pages):
        extracted = page.extract_text()
        if extracted:
            text += extracted

        # Limit the text to 1500 characters per page for each summary
        text_chunk = text[:1500]
        summary = summarize_with_retry(text_chunk)
        print(f"Summary for page {page_num + 1}: {summary}")

        summary_data = {
            "page": page_num + 1,
            "summary": summary
        }

        summary_data_list.append(summary_data)

    # Step 2: Save the summaries to a JSON file
    output_file = "summaries.json"
    try:
        with open(output_file, 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_data.extend(summary_data_list)

    with open(output_file, 'w') as f:
        json.dump(existing_data, f, indent=4)

    return "Summarization complete"
