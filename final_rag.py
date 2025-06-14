import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = None
full_dataset_text = ""

def load_and_embed_docs():
    global vectorstore, full_dataset_text
    folder_path = "data"
    documents = []

    all_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(Document(page_content=content, metadata={"source": filename}))
                all_text += content + "\n\n"

    full_dataset_text = all_text.strip()

    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(chunks, embedding_model)

def is_nepali(text):
    return any('\u0900' <= ch <= '\u097F' for ch in text)

def query_gemini(prompt: str) -> str:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        st.error(f"Gemini API error: {response.status_code} {response.text}")
        return ""

def answer_question(question: str, top_k=5):
    if vectorstore is None:
        st.error("Vectorstore not initialized!")
        return ""

    lang = "नेपाली" if is_nepali(question) else "English"

    docs = vectorstore.similarity_search(question, k=top_k)
    retrieved_text = "\n\n---\n\n".join([doc.page_content for doc in docs])

    prompt = (
     f"तल दिइएको सन्दर्भमा आधारित रही मात्र उत्तर दिनुहोस्। "
    f"यदि जवाफ पत्ता लगाउन सकिने जानकारी छैन भने, 'Out of context' मात्र लेख्नुहोस्।\n\n"
    f"Context:\n{full_dataset_text}\n\n"
    f"प्रश्न: {question}\n\n"
    f"उत्तर नेपाली भाषामा दिनुहोस्।"
    if lang == "नेपाली"
    else
    f"Answer the following question based **only on the provided context**. "
    f"If the answer is not found, reply exactly with: Out of context.\n\n"
    f"Context:\n{full_dataset_text}\n\n"
    f"Question: {question}\n\n"
    f"Answer in English."
    )

    return query_gemini(prompt)

def main():
    st.title("📄 Nepali + English ChatRAG with Gemini + LangChain Embeddings")

    with st.spinner("Loading and embedding documents..."):
        load_and_embed_docs()

    st.success("✅ Documents loaded and embedded!")

    question = st.text_input("Ask your question (English or Nepali):")

    if question:
        with st.spinner("Getting answer from Gemini..."):
            answer = answer_question(question, top_k=7)
            st.markdown(f"**Answer:** {answer}")

if __name__ == "__main__":
    main()
