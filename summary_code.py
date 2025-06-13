import fitz  
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env file
api_key = os.getenv("GOOGLE_API_KEY")


# Configure Gemini API with your key
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_text_from_pdf(pdf_file):
    # pdf_file is a file-like object (e.g., from Streamlit uploader)
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def summarize_pdf(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    prompt = (
        "Please read the following PDF text and provide a concise summary in simple paragraph and no markdown:\n\n"
        f"{text[:12000]}"  # Gemini input size limit
    )
    response = model.generate_content(prompt)
    return response.text
