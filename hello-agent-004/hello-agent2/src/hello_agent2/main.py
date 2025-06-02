import os
import openai
import asyncio
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("Api_Key")

async def chat():
    print("🤖 Async Chatbot ready! Type 'exit' to quit.")

    while True:
        user_input = await asyncio.to_thread(input, "You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",  # apni subscription ke mutabiq change karein
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        answer = response.choices[0].message.content
        print("Assistant:", answer)

if __name__ == "__main__":
    asyncio.run(chat())
