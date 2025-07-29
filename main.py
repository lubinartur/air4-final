from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Опционально: разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "sk-or-..."  # Вставь сюда свой ключ или передай через env

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        chat_id = data.get("chat_id")

        if not message or not chat_id:
            return {"error": "Missing message or chat_id"}

        # Подготовка запроса к OpenRouter
        payload = {
            "model": "mistral/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "Ты — локальный помощник, отвечай коротко, по делу."},
                {"role": "user", "content": message}
            ]
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourdomain.com",  # или твой реальный сайт
            "X-Title": "ar4gpt"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            if response.status_code != 200:
                return {
                    "error": f"OpenRouter error {response.status_code}",
                    "details": response.text
                }

            res = response.json()
            reply = res["choices"][0]["message"]["content"]
            return {"reply": reply, "chat_id": chat_id}

    except Exception as e:
        return {"error": str(e)}
