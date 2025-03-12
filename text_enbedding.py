import os
from transformers import AutoTokenizer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from document_loader import extract_text

# Set FAISS database path
DB_FAISS_PATH = "faiss_vectorstore"

# Load the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=500, chunk_overlap=100):
    """Splits text into token-based chunks ensuring uniform size."""
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    tokens = tokenizer.encode(text, truncation=False)  # Tokenize full text
    
    chunks = []
    for i in range(0, len(tokens), chunk_size - chunk_overlap):
        chunk_tokens = tokens[i: i + chunk_size]
        chunk_text = tokenizer.decode(chunk_tokens)  # Convert tokens back to text
        chunks.append(chunk_text)
    
    return chunks

def embed_and_store(chunks):
    """Embeds text chunks and stores them in FAISS, replacing any previous data."""
    db = FAISS.from_texts(chunks, embedding_model)
    db.save_local(DB_FAISS_PATH)
    print(f"Successfully stored {len(chunks)} chunks in FAISS.")
