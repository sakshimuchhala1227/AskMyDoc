# AskMyDoc - Document-Based Chatbot

## Overview

AskMyDoc is a document-based chatbot that allows users to upload documents and query them for relevant information. It extracts text from various file formats, stores embeddings in a FAISS vector database, and retrieves relevant content to answer user queries using Google's Gemini API. The chatbot strictly provides responses based only on the content within the uploaded documents and does not generate answers beyond the provided data.

## Features

- Supports multiple document formats: PDF, DOCX, TXT, CSV, XLSX, PPTX
- Uses FAISS for efficient text retrieval
- Embeds text using `sentence-transformers/all-MiniLM-L6-v2`
- Queries Google's Gemini API for responses
- Streamlit-based web interface for easy interaction
- Ensures responses are strictly based on provided documents and does not generate information beyond them

## Workflow

1. **Upload a Document**: Users upload a document via the Streamlit UI.
2. **Text Extraction**: The system extracts text from the uploaded document.
3. **Chunking and Embedding**: The text is split into chunks and embedded using `sentence-transformers/all-MiniLM-L6-v2`.
4. **Storing in FAISS**: The embedded text chunks are stored in a FAISS vector database.
5. **User Query**: The user enters a query through the chat interface.
6. **Retrieval and Response Generation**: Relevant document chunks are retrieved using FAISS, and Gemini API generates a response strictly based on the retrieved content.
7. **Response Display**: The chatbot returns an answer within the Streamlit UI.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/askmydoc.git
cd askmydoc
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate  
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

### 1. Start the Streamlit App

```bash
streamlit run streamlit.py
```

### 2. Upload Documents

- Use the sidebar to upload a document.
- The system will extract, embed, and store the text in FAISS.

### 3. Ask Questions

- Enter a query related to the uploaded document.
- The chatbot retrieves relevant document chunks and queries Gemini for a response.

## Project Structure

```
askmydoc/
├── faiss_vectorstore/          # FAISS database storage
├── document_loader.py          # Handles document text extraction
├── text_enbedding.py           # Chunks and embeds text into FAISS
├── main.py                     # FAISS retrieval + Gemini API call
├── streamlit.py                # Streamlit UI for chatbot
├── requirements.txt            # Required Python packages
├── .env.example                # Example .env file for API keys
└── README.md                   # Project documentation
```




