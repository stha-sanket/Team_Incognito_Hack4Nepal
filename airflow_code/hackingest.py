from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def ingest_documents(persist_dir=None):
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    persist_directory = persist_dir if persist_dir else os.path.join(current_dir, "chroma_db")
    
    # Initialize embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Initialize document storage
    documents = []
    
    # Read all text files from the data directory
    print(f"Reading documents from {data_dir}...")
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(Document(page_content=content, metadata={"source": filename}))
                print(f"Loaded {filename}")

    # Split documents into chunks
    print("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    
    # Create and persist the vector store
    print(f"Creating vector store at {persist_directory}...")
    # Ensure the directory exists
    os.makedirs(persist_directory, exist_ok=True)
    
    # Create the vector store (persistence is automatic in Chroma >= 0.4.0)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    
    print(f"Vector store created and saved to {persist_directory}")
    return persist_directory  # Return the directory path for verification

if __name__ == "__main__":
    ingest_documents() 