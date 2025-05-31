import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Gemini API Key (Store securely in production)
GEMINI_API_KEY = "AIzaSyBKLX3hDmlVeZQaQKABy8GZwGCiJZ5mwA4"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# Query Gemini
def query_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error communicating with Gemini: {e}"

# PDF text extraction
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Streamlit UI
st.set_page_config(page_title="Gemini Chatbot", layout="wide")
st.title("🤖 Chat with Gemini – فارسی + English | 📄 PDF Q&A")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# PDF upload
uploaded_file = st.file_uploader("📄 Upload a PDF (Optional)", type="pdf")
pdf_text = ""
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF content loaded.")

# User input
user_input = st.text_area("💬 Enter your question (English یا فارسی):", height=100)

# Send message
if st.button("Send") and user_input.strip():
    # Include PDF content in the prompt if uploaded
    prompt = ""
    if pdf_text:
        prompt += f"Here is some content from a PDF:\n{pdf_text[:3000]}\n\n"
    prompt += f"User: {user_input}\nAI:"

    with st.spinner("💬 Gemini is thinking..."):
        reply = query_gemini(prompt)

    # Update chat history
    st.session_state.chat_history.append((user_input, reply))

# Display conversation history
if st.session_state.chat_history:
    st.subheader("📝 Chat History")
    for user_msg, bot_reply in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Gemini:** {bot_reply}")
        st.markdown("---")
