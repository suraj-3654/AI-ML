# 🧠 Advanced RAG Research Copilot: User & Developer Guide

This repository contains a production-grade **Retrieval-Augmented Generation (RAG)** system designed to parse, index, and reason over complex technical research papers. It features a high-performance **FastAPI** backend and an interactive **Streamlit** frontend.

---

## 🚀 Key Features

* **PDF Ingestion & Indexing**: Upload and process multi-page technical documents.
* **Parent-Child Retrieval**: Uses small "Child" chunks for precise vector matching and large "Parent" chunks to provide the LLM with full context.
* **Multi-Query Expansion**: Automatically rephrases user queries into multiple variations to capture all relevant document segments.
* **RAG Triad Evaluation**: Every answer is audited by a "Judge LLM" for:
    * **Faithfulness**: Ensuring no hallucinations (answer is grounded in PDF).
    * **Relevance**: Ensuring the answer matches the user's intent.
    * **Context Precision**: Measuring the quality of the retrieved text.
* **Automated Logging**: All queries and quality scores are saved to `rag_performance_logs.csv` for performance tracking.

---

## 🛠️ Tech Stack

* **LLM**: Llama 4 Scout (17B-16E) via Groq
* **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (384 Dimensions)
* **Vector Store**: ChromaDB
* **Frameworks**: LangChain, FastAPI, Streamlit
* **Language**: Python 3.9+

---

## 🏗️ Complete Setup & Run Instructions

### Step 1: Clone Repository & Navigate
```bash
git clone <your-repo-url>
cd rag-research-copilot
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
```bash
# Copy and edit the example config
cp .env.example .env
# Edit .env with your API keys:
# GROQ_API_KEY=your_groq_key
# CHROMA_PERSISTENT_DIR=./chroma_db
```

### Step 6: Start Backend (FastAPI Server)
**Terminal 1:**
```bash
python backend.py
```
*Backend runs on `http://localhost:8000`*
*API docs: `http://localhost:8000/docs`*

### Step 7: Start Frontend (Streamlit App)
**Terminal 2:** (Keep backend running in Terminal 1)
```bash
streamlit run frontend.py
```
*Frontend runs on `http://localhost:8501`*

---

## 🔄 Development Workflow

### Fresh Start (Reset Everything)
```bash
# 1. Stop all processes (Ctrl+C)
# 2. Deactivate & remove environment
deactivate
rm -rf venv chroma_db/

# 3. Recreate from scratch
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your keys
```

### Quick Restart (Keep Environment)
```bash
# Stop processes (Ctrl+C), then:
python backend.py    # Terminal 1
streamlit run frontend.py  # Terminal 2
```

### Production Deployment
```bash
# Backend with Uvicorn (recommended for production)
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

# Frontend with Docker (optional)
docker build -t rag-copilot .
docker run -p 8501:8501 rag-copilot
```

---

## 🧪 Testing the Pipeline

1. **Backend Health Check**: `curl http://localhost:8000/health`
2. **Upload PDF**: Via Streamlit frontend → "Upload PDF" button
3. **Query Test**: Ask "What is the main contribution of this paper?"
4. **Check Logs**: View `rag_performance_logs.csv` for RAG scores

**Expected Scores:**
- Faithfulness: >0.9
- Relevance: >0.85
- Context Precision: >0.8

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `GROQ_API_KEY` error | Check `.env` file |
| Backend 500 error | Check `backend.py` logs |
| ChromaDB corruption | `rm -rf chroma_db/` |
| Streamlit not loading | `streamlit run frontend.py --server.port 8501` |

---

## 📊 Performance Monitoring

All interactions logged to `rag_performance_logs.csv`: