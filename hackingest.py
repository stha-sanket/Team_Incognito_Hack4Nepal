from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def ingest_documents():
    # Initialize embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Initialize document storage
    folder_path = "data"
    documents = []
    
    # Read all text files from the data directory
    print("Reading documents...")
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(Document(page_content=content, metadata={"source": filename}))
                print(f"Loaded {filename}")

    # Split documents into chunks
    print("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    
    # Create and persist the vector store
    print("Creating vector store...")
    persist_directory = "chroma_db"
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    
    print(f"Vector store created and saved to {persist_directory}")
    return "Ingestion completed successfully!"

if __name__ == "__main__":
    ingest_documents() 