import os
import csv
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.stores import InMemoryStore
from langchain_classic.retrievers import ParentDocumentRetriever, MultiQueryRetriever
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uvicorn

load_dotenv()
app = FastAPI()

# --- 1. INITIALIZE MODELS ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)
eval_llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

# --- 2. VECTOR STORE & RETRIEVER SETUP ---
vectorstore = Chroma(collection_name="networking_rag", embedding_function=embeddings, persist_directory="./chroma_db")
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=300),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=1500),
)

advanced_retriever = MultiQueryRetriever.from_llm(retriever=retriever, llm=llm)

# --- 3. RAG CHAIN SETUP ---
system_prompt = (
    "You are a strict Research Assistant. Use ONLY the provided context "
    "from the research papers to answer. \n\n"
    "RULES: If the answer isn't in the context, say you don't know.\n\n"
    "CONTEXT:\n{context}"
)
prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(advanced_retriever, combine_docs_chain)

# --- 4. UTILITIES ---
def log_performance(query, scores):
    with open("rag_performance_logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), query, scores.replace("\n", " | ")])

def evaluate_triad(query, context, answer):
    eval_prompt = f"Rate 0-10.\nQUERY: {query}\nCONTEXT: {context}\nANSWER: {answer}\nFormat: Faithfulness: [X]/10 Relevance: [X]/10 Precision: [X]/10 Reasoning: [1 sentence]"
    try:
        return eval_llm.invoke(eval_prompt).content
    except:
        return "Evaluation Failed"

# --- 5. API ENDPOINTS ---

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Save temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Load and index
    loader = PyPDFLoader(temp_path)
    docs = loader.load()
    retriever.add_documents(docs, ids=None)
    
    os.remove(temp_path)
    return {"message": f"Successfully indexed {file.filename}"}

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    result = rag_chain.invoke({"input": request.query})
    answer = result["answer"]
    source_context = "\n".join([doc.page_content for doc in result["context"]])
    triad_report = evaluate_triad(request.query, source_context, answer)
    log_performance(request.query, triad_report)
    
    return {"answer": answer, "evaluation": triad_report}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)