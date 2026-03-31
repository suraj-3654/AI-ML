# 🏗️ GraphRAG Codebase Architect

**A Full-Stack AI tool that maps your codebase and predicts code change impacts.**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![GraphRAG](https://img.shields.io/badge/GraphRAG-Logic-blueviolet?style=for-the-badge)](https://github.com/microsoft/graphrag)

## 🌟 What It Does

This tool helps developers understand complex codebases instantly. It reads your code structure and creates a visual map of how everything connects.

**Key Features:**
- Maps Python backend + JavaScript frontend code together
- Predicts which files break when you change one file
- Groups similar code and explains what each group does
- Indexes repos in seconds (not hours)

---

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