from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_chatbot_response

app = FastAPI(title="JainBot")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True, 
)

class ChatRequest(BaseModel):
    query : str

@app.get("/")
async def root():
    return {"message":"JainBot Running Successfully"}

@app.post("/chat")
async def chat_endpoint(req:ChatRequest):
    user_input = req.query
    if not user_input:
        raise HTTPException(status_code=400, detail = "Query cannot be empty!")
    
    try:
        response = get_chatbot_response(user_input=user_input)
        return {"answer":response}

    except Exception as e:
        return {"answer": f"Error occured -> {e}"}