from fastapi import FastAPI, Depends
from pydantic import BaseModel

from .graph import aura_graph
from .tools import get_github_api
from .auth import verify_api_key


app = FastAPI(
    title="AURA AI Assistant",
    description="AI Unified Reasoning Assistant API",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "AURA FastAPI backend is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    result = aura_graph.invoke({
        "message": request.message,
        "route": "",
        "response": "",
        "tool_result": ""
    })

    return {
        "response": result["response"],
        "route": result["route"]
    }


@app.get("/api/github")
def github_api(api_key: bool = Depends(verify_api_key)):
    return get_github_api()