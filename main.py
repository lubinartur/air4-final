from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

class PromptRequest(BaseModel):
    message: str
    chat_id: int

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "mistralai/mistral-7b-instruct"

@app.post("/chat")
async def chat(req: PromptRequest):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "ar4gpt"
    }

    messages = [{"role": "user", "content": req.message}]
    
    payload = {
        "model": MODEL,
        "messages": messages,
    }

    async with httpx.AsyncClient() as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        reply = data["choices"][0]["message"]["content"]

        return {
            "reply": reply,
            "chat_id": req.chat_id  # вернуть chat_id обратно, чтобы n8n мог его использовать
        }
