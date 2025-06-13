import streamlit as st
from rag_code import (
    extract_text_from_pdfs,
    split_into_chunks,
    build_vector_store,
    generate_answer
)

def main():
    st.set_page_config(page_title="Gemini PDF QA", page_icon="📘")

    st.markdown("<h1 style='text-align: center; color: teal;'>📘 Ask Your PDF</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload multiple PDFs and ask questions using Gemini Pro!</p>", unsafe_allow_html=True)

    st.divider()

    question = st.text_input("🔎 What do you want to know from the uploaded PDFs?")

    if question:
        with st.spinner("🤖 Thinking..."):
            response = generate_answer(question)
            st.success("✅ Answer ready!")
            st.markdown(f"**Answer:** {response}")

    st.divider()

    with st.sidebar:
        st.header("📄 Upload PDFs")
        pdf_files = st.file_uploader("Upload one or more PDF files", type=["pdf"], accept_multiple_files=True)

        if st.button("🚀 Submit & Process"):
            if pdf_files:
                with st.spinner("🔧 Extracting and indexing..."):
                    text = extract_text_from_pdfs(pdf_files)
                    chunks = split_into_chunks(text)
                    build_vector_store(chunks)
                    st.sidebar.success("✅ PDFs processed and indexed!")
            else:
                st.sidebar.warning("⚠️ Please upload at least one PDF.")

if __name__ == "__main__":
    main()
