import streamlit as st
import requests

st.set_page_config(page_title="Codebase Architect", layout="wide")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "repo_indexed" not in st.session_state:
    st.session_state.repo_indexed = False

st.title("🏗️ GraphRAG Codebase Architect")

with st.sidebar:
    st.header("🛠️ Controls")
    repo_url = st.text_input("GitHub Repo URL", placeholder="https://github.com/user/repo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Index Repo"):
            with st.spinner("Analyzing..."):
                res = requests.post("http://localhost:8000/analyze", json={"repo_url": repo_url})
                if res.status_code == 200:
                    st.session_state.repo_indexed = True
                    st.success(f"Indexed: {res.json()['project']}")
                else:
                    st.error("Indexing failed.")

    with col2:
        # THE CLEAR BUTTON
        if st.button("🗑️ Clear All"):
            res = requests.post("http://localhost:8000/clear")
            if res.status_code == 200:
                # Reset Streamlit state
                st.session_state.messages = []
                st.session_state.repo_indexed = False
                st.rerun() # Refresh the UI

st.divider()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask about the architecture..."):
    if not st.session_state.repo_indexed:
        st.error("Please index a repository first!")
    else:
        # Add user message to UI
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from Backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                res = requests.post("http://localhost:8000/ask", json={"query": prompt})
                if res.status_code == 200:
                    answer = res.json()['answer']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Backend error.")