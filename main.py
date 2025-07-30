from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# CORS — можно оставить, если вдруг нужно из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ключ OpenRouter — можешь задать в .env или вписать напрямую
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "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"

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        chat_id = data.get("chat_id")

        if not message or not chat_id:
            return {"error": "Missing message or chat_id"}

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "Ты — локальный помощник, отвечай коротко, по делу."},
                {"role": "user", "content": message}
            ]
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ar4gpt.onrender.com",  # Укажи свой домен, если хочешь
            "X-Title": "ar4gpt"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)

        if response.status_code != 200:
            return {
                "input": {"chat_id": chat_id},
                "error": f"OpenRouter error {response.status_code}",
                "details": await response.json()
            }

        try:
            res = response.json()
            reply = res["choices"][0]["message"]["content"]
        except Exception as parse_err:
            return {
                "input": {"chat_id": chat_id},
                "error": f"Response parse error: {str(parse_err)}",
                "raw_response": await response.aread()
            }

        return {
            "input": {"chat_id": chat_id},
            "reply": reply
        }

    except Exception as e:
        return {
            "input": {"chat_id": data.get("chat_id")},
            "error": f"Internal server error: {str(e)}"
        }
