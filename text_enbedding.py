import os
from transformers import AutoTokenizer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from document_loader import extract_text  # Ensure this function correctly extracts text from various formats

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

# if __name__ == "__main__":
#     file_path = r"F:\8th sem\cloud computing\cloudcomputing.docx"

#     if os.path.exists(file_path):
#         extracted_text = extract_text(file_path)
        
#         if extracted_text:
#             print("\nText extracted successfully. Processing embeddings...\n")
#             chunks = chunk_text(extracted_text)
#             embed_and_store(chunks)
#         else:
#             print("Failed to extract text from the file.")
#     else:
#         print("File not found. Please check the path.")

def process_uploaded_file(uploaded_file):
    """Processes uploaded file, extracts text, chunks it, and stores embeddings."""
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        extracted_text = extract_text(temp_path)
        os.remove(temp_path)  # Clean up temporary file

        if extracted_text:
            chunks = chunk_text(extracted_text)
            num_chunks = embed_and_store(chunks)
            return f"Successfully stored {num_chunks} text chunks in FAISS."
        else:
            return "Failed to extract text from the file."

    return "No file uploaded."