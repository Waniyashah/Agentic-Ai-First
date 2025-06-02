import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("Api-Key")

print(f"API Key loaded: '{API_KEY}'")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-v3-base:free"

def ask_openrouter(question):
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": MODEL,
            "messages": [
                {"role": "user", "content": question}
            ]
        })
    )
    data = response.json()
    print("Full API Response:", data)
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error or no answer: {data}"

if __name__ == "__main__":
    answer = ask_openrouter("Hello, is mera setup sahi hai?")
    print("Answer:", answer)
