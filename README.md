# 🧾 Legal Document Summarizer using LangChain

## 📌 Project Title
**Legal Document Summarizer**: Build a summarization tool using **LangChain** to condense lengthy legal documents.

---

## 📖 Project Overview

This project is designed to help users quickly understand the contents of lengthy legal PDF documents by providing concise and clear summaries. It leverages **LangChain**, integrated with **Hugging Face’s** summarization models, to extract and summarize essential information using natural language processing (NLP).

The application includes both a **command-line backend script** (`summarizer.py`) and a **user-friendly Streamlit web interface** (`app.py`).

---

## 🚀 Features

- 📄 Upload and read legal documents in PDF format
- 🧠 Use Hugging Face models via LangChain for summarization
- ✅ Handles large PDFs by chunking and retries
- 💾 Stores results in `summaries.json`
- 🔐 Keeps API tokens secure via `.env` file
- 🌐 Streamlit-based user interface for non-technical users

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/raji51123/lds.git
cd lds
