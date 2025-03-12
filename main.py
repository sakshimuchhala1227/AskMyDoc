import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Configuration
DB_FAISS_PATH = "faiss_vectorstore"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-1.5-flash"

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# Load FAISS Retriever
def load_faiss():
    """Loads FAISS vector store and returns a retriever."""
    db = FAISS.load_local(
        DB_FAISS_PATH, 
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        allow_dangerous_deserialization=True
    )
    return db.as_retriever()

# Query Gemini API
def query_gemini(prompt):
    """Calls Gemini API to generate a response."""
    response = model.generate_content(prompt)
    return response.text if response else "Error: No response from Gemini."

# Generate response using FAISS + Gemini LLM
def generate_rag_response(query):
    """Uses FAISS retriever to fetch relevant chunks, then queries Gemini."""
    retriever = load_faiss()
    relevant_docs = retriever.invoke(query)

    retrieved_text = "\n".join([doc.page_content for doc in relevant_docs])
    
    prompt = f"Use the following retrieved information to answer the query:\n\n{retrieved_text}\n\nUser Query: {query}"
    
    return query_gemini(prompt)
