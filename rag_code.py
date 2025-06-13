import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

DATA_FOLDER = "data"
CHROMA_DIR = "chroma_db"

# Step 1: Read and extract text from PDFs
def extract_text_from_pdfs(folder=DATA_FOLDER):
    all_text = ""
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            path = os.path.join(folder, file)
            reader = PdfReader(path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
    return all_text

# Step 2: Split text
def split_into_chunks(text, chunk_size=4000, chunk_overlap=400):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

# Step 3: Create vectorstore
def build_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma.from_texts(chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    vectordb.persist()
    print("[INFO] Vector store built.")

def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

# Step 4: Setup QA
def load_qa_pipeline():
    prompt = PromptTemplate(
        template="""
Answer the question using the context below. Be detailed.
If the context does not contain the answer, say: "Answer is not available in the context."

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"]
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    return load_qa_chain(llm, chain_type="stuff", prompt=prompt)

# Step 5: Ask question
def generate_answer(question):
    vectordb = load_vector_store()
    docs = vectordb.similarity_search(question)
    if not docs:
        return "Answer is not available in the context."
    qa_chain = load_qa_pipeline()
    result = qa_chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return result["output_text"]

# One-time build
if not os.path.exists(CHROMA_DIR):
    print("[INFO] Building vectorstore from existing PDFs in 'data/'...")
    raw_text = extract_text_from_pdfs()
    chunks = split_into_chunks(raw_text)
    build_vector_store(chunks)
else:
    print("[INFO] Existing vectorstore loaded.")
