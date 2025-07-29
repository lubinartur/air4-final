from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(msg: Message):
    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "Ты умный помощник."},
            {"role": "user", "content": msg.message}
        ]
    )
    return {"response": response.choices[0].message["content"]}
