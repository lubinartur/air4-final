import os
from fastapi import FastAPI
import openai

app = FastAPI()

openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

@app.get("/")
def root():
    return {"message": "AR4GPT is alive!"}

@app.post("/chat")
def chat(prompt: str):
    response = openai.ChatCompletion.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return {"reply": response['choices'][0]['message']['content']}
