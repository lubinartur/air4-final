from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import openai

load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.get("/")
def root():
    return {"message": "AR4GPT is live."}


@app.post("/api/v1/gpt4")
async def gpt4(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    system = data.get("system", "You are a helpful assistant.")

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
        )
        return JSONResponse(content={"text": response.choices[0].message.content})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
