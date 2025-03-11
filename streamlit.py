import streamlit as st
from document_loader import extract_text
from text_enbedding import chunk_text, embed_and_store
from main import generate_rag_response

# Streamlit UI Configuration
st.set_page_config(page_title="Document-Based Chatbot", layout="wide")

st.title("AskMyDoc")

# Sidebar for Document Upload
st.sidebar.header("Upload Documents")
uploaded_file = st.sidebar.file_uploader(
    "Upload your document", 
    type=["pdf", "docx", "txt", "xlsx", "csv", "pptx"],
    accept_multiple_files=False
)

if uploaded_file:
    st.sidebar.info(f"Processing {uploaded_file.name}...")
    
    # Read file content
    file_bytes = uploaded_file.read()
    
    # Extract text
    extracted_text = extract_text(uploaded_file.name, file_bytes)
    
    if extracted_text:
        chunks = chunk_text(extracted_text)
        embed_and_store(chunks)
        st.sidebar.success("Document processed successfully!")
    else:
        st.sidebar.error("Failed to extract text from the document.")

# Chatbot Section
st.header("Chat with Your Document")
user_query = st.text_area("Enter your question:")

if st.button("Ask"):
    if user_query.strip():
        response = generate_rag_response(user_query)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please enter a question.")
