from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from scan_code import CodebaseArchitect 

app = FastAPI()
# Global instance
architect = CodebaseArchitect()

class RepoRequest(BaseModel):
    repo_url: str

class QueryRequest(BaseModel):
    query: str

@app.post("/analyze")
async def analyze_repo(req: RepoRequest):
    try:
        # If a previous repo exists, clean it up first
        if architect.temp_dir:
            architect.cleanup()
        
        architect.clone_and_analyze(req.repo_url)
        return {"status": "success", "project": architect.project_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(req: QueryRequest):
    if not architect.graph:
        raise HTTPException(status_code=400, detail="No repo analyzed yet.")
    answer = architect.ask(req.query)
    return {"answer": answer}

@app.post("/clear")
async def clear_session():
    """Wipes the temp directory and resets the architect state."""
    try:
        architect.cleanup()
        # Reset internal variables
        architect.triples = []
        architect.communities = {}
        architect.community_summaries = []
        architect.nodes = []
        architect.graph = None
        architect.project_name = ""
        return {"status": "session cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    architect.cleanup()