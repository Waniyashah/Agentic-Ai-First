from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("Open_Ai_Key")

def openai():
    response = completion(
        model = "openrouter/google/gemma-3n-e4b-it:free",
        messages = [{
            "content": "Hello, how are you?",
            "role": "user"
        }],    
        api_base="https://openrouter.ai/api/v1",
        api_key=API_KEY
    )
    print(response.choices[0].message.content)

def gemini():
    response = completion(
        model = "openrouter/meta-llama/llama-3.3-8b-instruct:free",
        messages = [{
            "content": "Hello, how are you?",
            "role": "user"
        }],
        api_base="https://openrouter.ai/api/v1",
        api_key= API_KEY
    )
    print(response.choices[0].message.content)

def gemini1():
    response = completion(
        model = "openrouter/mistralai/devstral-small:free",
        messages = [{
            "content": "Hello, how are you?",
            "role": "user"
        }],
        api_base="https://openrouter.ai/api/v1",
        api_key=API_KEY
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    openai()
    gemini()
    gemini1()