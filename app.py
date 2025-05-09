import streamlit as st
import json
import os
from PyPDF2 import PdfReader
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print all environment variables to verify loading
print(os.environ)

# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")

# Check if the token is set correctly
if hf_token is None:
    st.error("Hugging Face token is not set. Please set it as an environment variable (HF_TOKEN).")
    st.stop()

# Initialize the inference client
client = InferenceClient(token=hf_token)

# Streamlit App UI
st.title("🧾 Legal Document Summarizer")

# File uploader
uploaded_file = st.file_uploader("Upload a legal PDF document", type="pdf")

if uploaded_file is not None:
    # Read PDF
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # Truncate text to stay within model limits (1500 characters)
    text = text[:1500]

    st.subheader("Extracted Text Preview")
    st.write(text[:1000] + "...")  # Show the first 1000 characters

    # Summarize button
    if st.button("Summarize"):
        try:
            # Use summarization model (facebook/bart-large-cnn)
            response = client.summarization(
                text=text,
                model="facebook/bart-large-cnn"
            )
            summary = response.get('summary_text', 'Summary not available.')
        except Exception as e:
            summary = f"Error generating summary: {str(e)}"

        # Display summary
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

        with open("summaries.json", "w") as f:
            json.dump(existing_data, f, indent=4)

        st.success("✅ Summary saved to summaries.json")
