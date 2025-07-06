from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent import process_agent_message


class AgentRequest(BaseModel):
    message: str


app = FastAPI()


@app.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    try:
        reply = await process_agent_message(request.message)
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Hello World"}
