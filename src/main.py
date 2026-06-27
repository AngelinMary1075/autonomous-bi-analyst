from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database import init_db
from src.agent import run_bi_agent

app = FastAPI(title="Autonomous BI Analyst API")

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

class QueryRequest(BaseModel):
    prompt: str

@app.post("/analytics/ask")
async def ask_analyst(request: QueryRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    
    result = run_bi_agent(request.prompt)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)