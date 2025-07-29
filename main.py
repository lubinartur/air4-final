import openai
import os

# Вставь свой OpenRouter API ключ сюда
openai.api_key = "sk-..."
openai.api_base = "https://openrouter.ai/api/v1"

# Список доступных моделей можно получить здесь: https://openrouter.ai/docs#models

response = openai.ChatCompletion.create(
    model="mistralai/mistral-7b-instruct",
    messages=[
        {"role": "system", "content": "Ты умный, токсично-доброжелательный ассистент. Отвечай кратко, но по делу. Стиль — как у лучшего друга-хакера."},
        {"role": "user", "content": "Что ты знаешь о Лунной сонате Бетховена?"}
    ]
)

print(response.choices[0].message.content)
