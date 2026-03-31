# 🏗️ GraphRAG Codebase Architect

**A Full-Stack AI Observability Tool for Automated System Mapping & Impact Analysis.**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![GraphRAG](https://img.shields.io/badge/GraphRAG-Logic-blueviolet?style=for-the-badge)](https://github.com/microsoft/graphrag)

## 🌟 Overview

The **Codebase Architect** is a specialized GraphRAG (Graph Retrieval-Augmented Generation) application designed to help developers onboard to complex repositories instantly. Unlike standard RAG which treats code as plain text, this tool uses **Static Analysis (AST)** and **Graph Theory** to understand the structural dependencies and functional intent of a system.

### 🎯 Key Capabilities
- **Polyglot Mapping:** Bridges the gap between Frontend (JS/TS) and Backend (Python) by identifying shared API contracts.
- **Blast Radius Analysis:** Uses Breadth-First Search (BFS) on a dependency graph to predict which modules will break if a specific file is modified.
- **Automated Summarization:** Clusters code into "Functional Neighborhoods" using the Leiden Algorithm and summarizes their architectural roles using Llama-4.
- **High-Speed Ingestion:** Implements Shallow Cloning and Thread-Pooled LLM requests to index medium-sized repos in seconds.

---

## 🛠️ Architecture



The system is built on a **Decoupled Microservice Architecture**:

1.  **Backend (FastAPI):**
    * **Ingestion:** Clones repos using `GitPython` (Depth=1).
    * **Parsing:** Extracts Abstract Syntax Trees (AST) for Python and Regex patterns for JS.
    * **Graph Engine:** Builds a directed dependency graph using `iGraph`.
    * **LLM Layer:** Orchestrates batched requests to Groq (Llama-3/4) for contextual summarization.
2.  **Frontend (Streamlit):**
    * Provides a chat-based interface for architectural queries.
    * Visualizes "Impact Alerts" when dangerous code changes are detected.

---

## 🚀 Getting Started


## 🛠️ How It Works

**Two main parts:**

### Backend (FastAPI)
- Clones your Git repo
- Reads code structure (Python AST + JS patterns)  
- Builds a dependency graph
- Uses AI (Llama) to summarize code purpose

### Frontend (Streamlit) 
- Chat interface for asking about your codebase
- Shows warnings for risky code changes
- Visual graphs of your code connections

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- [Free Groq API Key](https://console.groq.com/)

### 2. Setup
```bash
# Clone repo
git clone https://github.com/suraj-3654/AI-ML.git
cd AI-ML
git checkout devleop_code_achitect_with_graphrag

# Create virtual environment
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App

**Terminal 1 - Start Backend:**
```bash
uvicorn backend:app --port 8000 --reload
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

**Open your browser to:** `http://localhost:8501`

---

## 📚 Example Usage

1. Paste any GitHub repo URL
2. Click "Analyze Codebase" 
3. Ask questions like:
   - "What happens if I delete this file?"
   - "Show me all API endpoints"
   - "Explain this module's purpose"

---

## 🤔 Need Help?

- [Backend API Docs](http://localhost:8000/docs)
- Check `docs/` folder for advanced usage
- Join our [Discord](https://discord.gg/YOUR-DISCORD)

**Made with ❤️ for developers who hate reading other people's code.**