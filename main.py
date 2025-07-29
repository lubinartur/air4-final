from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

class PromptRequest(BaseModel):
    message: str
    chat_id: int

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL") or "mistralai/mistral-7b-instruct"

@app.post("/chat")
async def chat(req: PromptRequest):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourdomain.com",
            "X-Title": "ar4gpt"
        }

        messages = [{"role": "user", "content": req.message}]
        payload = {
            "model": MODEL,
            "messages": messages,
        }

        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )
            r.raise_for_status()
            data = await r.json()  # ← ОБЯЗАТЕЛЬНО await здесь

            reply = data["choices"][0]["message"]["content"]
            return {
                "reply": reply,
                "chat_id": req.chat_id
            }

    except Exception as e:
        return {
            "error": str(e),
            "model": MODEL,
            "key_set": bool(OPENROUTER_API_KEY),
            "input": req.dict()
        }
