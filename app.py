import streamlit as st
import google.generativeai as genai

# Gemini API Key (replace with secure method in production)
GEMINI_API_KEY = "AIzaSyBKLX3hDmlVeZQaQKABy8GZwGCiJZ5mwA4"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Query Gemini
def query_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error communicating with Gemini: {e}"

# Streamlit UI
st.set_page_config(page_title="Gemini Chatbot", layout="wide")
st.title("🤖 Chat with Gemini – فارسی + English")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_area("💬 Enter your question (English یا فارسی):", height=100)

# Send message
if st.button("Send") and user_input.strip():
    prompt = f"User: {user_input}\nAI:"
    with st.spinner("💬 Gemini is thinking..."):
        reply = query_gemini(prompt)
    st.session_state.chat_history.append((user_input, reply))

# Display chat history
if st.session_state.chat_history:
    st.subheader("📝 Chat History")
    for user_msg, bot_reply in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Gemini:** {bot_reply}")
        st.markdown("---")
