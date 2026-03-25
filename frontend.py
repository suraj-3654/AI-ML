import streamlit as st
import requests

st.set_page_config(page_title="Scout RAG Pro", page_icon="🧠", layout="wide")

st.title("🧠 Scout Research Copilot")

# Sidebar for Uploading
with st.sidebar:
    st.header("📂 Document Management")
    uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")
    
    if uploaded_file:
        if st.button("Index Document"):
            with st.spinner("Processing PDF..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post("http://127.0.0.1:8000/upload", files=files)
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error("Upload failed.")

    if st.button("Clear Chat"):
        st.session_state.messages = []

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "evaluation" in message:
            with st.expander("🔍 Quality Audit (RAG Triad)"):
                st.write(message["evaluation"])

user_prompt = st.chat_input("Ask about the paper...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            res = requests.post("http://127.0.0.1:8000/ask", json={"query": user_prompt})
            if res.status_code == 200:
                data = res.json()
                st.markdown(data["answer"])
                with st.expander("🔍 Quality Audit"):
                    st.write(data["evaluation"])
                st.session_state.messages.append({"role": "assistant", "content": data["answer"], "evaluation": data["evaluation"]})