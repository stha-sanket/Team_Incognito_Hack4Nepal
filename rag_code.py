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

def extract_text_from_pdfs(pdf_docs):
    full_text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text
    return full_text

def split_into_chunks(text, chunk_size=4000, chunk_overlap=400):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def build_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma.from_texts(
        chunks, 
        embedding=embeddings, 
        persist_directory="chroma_db"
    )
    vectorstore.persist()

def load_qa_pipeline():
    prompt = PromptTemplate(
        template="""
        Answer the question using the context below. Be as detailed as possible.
        If the answer is not in the context, say: "Answer is not available in the context."

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

def generate_answer(question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    documents = vectorstore.similarity_search(question)

    qa_chain = load_qa_pipeline()
    response = qa_chain({"input_documents": documents, "question": question}, return_only_outputs=True)

    return response["output_text"]
