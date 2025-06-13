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
    st.markdown("<p style='text-align: center;'>This bot answers questions based on the government document</p>", unsafe_allow_html=True)

    st.divider()

    question = st.text_input("🔎 What do you want to know from the stored PDFs?")

    if question:
        with st.spinner("🤖 Thinking..."):
            response = generate_answer(question)
            st.success("✅ Answer ready!")
            st.markdown(f"**Answer:** {response}")

    st.divider()

if __name__ == "__main__":
    main()
