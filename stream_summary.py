import streamlit as st
from summary_code import summarize_pdf

st.title("📄 Gemini PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Generating summary..."):
        summary = summarize_pdf(uploaded_file)
        st.subheader("Summary")
        st.write(summary)
else:
    st.info("Please upload a PDF file to summarize.")
