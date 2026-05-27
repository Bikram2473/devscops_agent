from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uvicorn
from agent import process_incident

app = FastAPI(title="DevSecOps Ingestion Webhook")

class ErrorLog(BaseModel):
    service_name: str
    error_type: str
    stack_trace: str
    timestamp: str

@app.post("/v1/triage/report")
async def report_incident(log: ErrorLog, background_tasks: BackgroundTasks):
    # Pass the log to the LangGraph agent in the background so the API doesn't hang
    background_tasks.add_task(process_incident, log.dict())
    return {"status", "Incident received. Agent is investigating."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0.", port=8000)