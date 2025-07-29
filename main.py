from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

# Получаем API-ключ из переменных окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root():
    return {"message": "ar4gpt is running"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages")

    if not messages:
        return {"error": "Missing 'messages' in request body"}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # или gpt-4, если есть доступ
        messages=messages
    )
    return response
