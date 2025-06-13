import streamlit as st
from summary_code import summarize_pdf
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDJ-yCECLpPPSMUL4Ua6a8gqEmSeMYzcfA")
model = genai.GenerativeModel("gemini-2.0-flash")

# Set dark theme page config
st.set_page_config(page_title="Summarizer + Chatbot", layout="centered")

# Apply dark-friendly styling
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .user-bubble {
            background-color: #2c2c2c;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: right;
            color: #6debd7;
        }
        .bot-bubble {
            background-color: #3a3a3a;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: left;
            color: white;
        }
        .chat-input {
            background-color: #2c2c2c;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("📄  PDF Summary + 💬 Chatbot")

# PDF Upload and Summarizer
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Summarizing..."):
        summary = summarize_pdf(uploaded_file)
    st.subheader("📘 Summary")
    st.write(summary)
    st.markdown("---")
else:
    st.info("📎 Upload a PDF to generate summary.")

# Chat section
st.subheader("💬 Chat with Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for user, bot in st.session_state.chat_history:
    st.markdown(f"<div class='user-bubble'><b>YOU:</b> {user}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-bubble'><b>Bot:</b> {bot}</div>", unsafe_allow_html=True)

# Input box at the bottom
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask something...", placeholder="Type here...", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    with st.spinner("Thinking..."):
        response = model.generate_content(user_input)
        answer = response.text
        st.session_state.chat_history.append((user_input, answer))
        st.rerun()
