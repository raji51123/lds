'''import streamlit as st
import json
from PyPDF2 import PdfReader
from huggingface_hub import InferenceClient

# Hugging Face token
hf_token = os.getenv("HF_TOKEN") 
client = InferenceClient(token=hf_token)

# Title
st.title("🧾 Legal Document Summarizer")

uploaded_file = st.file_uploader("Upload a legal PDF document", type="pdf")

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # Limit the text size
    text = text[:3000]

    st.subheader("Extracted Text Preview")
    st.write(text[:1000] + "...")

    if st.button("Summarize"):
        try:
            response = client.summarization(text=text, model="facebook/bart-large-cnn")
            summary = response.get('summary_text', '')
        except Exception as e:
            summary = f"Error generating summary: {str(e)}"

        # Display summary
        st.subheader("Summary")
        st.write(summary)

        # Save to summaries.json
        try:
            with open("summaries.json", "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        existing_data.append({
            "document": uploaded_file.name,
            "summary": summary
        })

        with open("summaries.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        st.success("✅ Summary saved to summaries.json")
'''
import streamlit as st
import json
import os
from PyPDF2 import PdfReader
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load Hugging Face API token from .env file
load_dotenv()

# Load the token from the environment variable
hf_token = os.getenv("HUGGINGFACE_API_TOKEN")

# Check if the token is provided
if hf_token is None:
    st.error("Hugging Face token is not set. Please set it as an environment variable (HUGGINGFACE_API_TOKEN).")
    st.stop()

# Initialize the inference client with the Hugging Face token
client = InferenceClient(token=hf_token)

# Streamlit App UI
st.title("🧾 Legal Document Summarizer")

# File upload component
uploaded_file = st.file_uploader("Upload a legal PDF document", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # Truncate text to stay within model limits (1500 characters max)
    text = text[:1500]

    # Display extracted text preview
    st.subheader("Extracted Text Preview")
    st.write(text[:1000] + "...")

    # Button to trigger summarization
    if st.button("Summarize"):
        try:
            # Use Hugging Face model for summarization
            response = client.summarization(
                text=text,
                model="facebook/bart-large-cnn"
            )
            summary = response.get('summary_text', 'Summary generation failed.')
        except Exception as e:
            summary = f"Error generating summary: {str(e)}"

        # Display the summary
        st.subheader("Summary")
        st.write(summary)

        # Save the summary to a JSON file
        try:
            with open("summaries.json", "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        existing_data.append({
            "document": uploaded_file.name,
            "summary": summary
        })

        # Write the updated summary data to the JSON file
        with open("summaries.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        st.success("✅ Summary saved to summaries.json")
