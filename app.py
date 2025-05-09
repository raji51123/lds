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
load_dotenv()

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")
if hf_token is None:
    st.error("Hugging Face token is not set. Please set it as an environment variable (HF_TOKEN).")
    st.stop()

# Initialize the inference client
client = InferenceClient(token=hf_token)

# Streamlit App UI
st.title("🧾 Legal Document Summarizer")

uploaded_file = st.file_uploader("Upload a legal PDF document", type="pdf")

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # Truncate text to stay within model limits
    text = text[:1500]

    st.subheader("Extracted Text Preview")
    st.write(text[:1000] + "...")

    if st.button("Summarize"):
        try:
            # Use summarization model
            response = client.summarization(
                text=text,
                model="facebook/bart-large-cnn"
            )
            summary = response.get('summary_text', '')
        except Exception as e:
            summary = f"Error generating summary: {str(e)}"

        # Display summary
        st.subheader("Summary")
        st.write(summary)

        # Save the summary to JSON
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
