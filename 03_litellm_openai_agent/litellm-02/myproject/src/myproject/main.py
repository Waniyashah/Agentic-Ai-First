import os
from dotenv import load_dotenv
import chainlit as cl
from litellm import completion
import json

# Load environment variables from .env file
load_dotenv()

# Environment variable ka naam aapke code mein "Gemini_Api_Key" hai,
# lekin variable ka naam uppercase aur underscore hona chahiye for consistency.
OPENROUTER_API_KEY = os.getenv("Gemini_Api_Key")  # Check .env mein ye same hona chahiye

BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please ensure it is defined in your .env file")

@cl.on_chat_start
async def start():
    # Chat history ko sahi key se initialize karen
    cl.user_session.set("Chat_history", [])
    await cl.Message(content="🤖 Welcome to the wano's AI Assistant. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="🤔 Thinking...")
    await msg.send()

    # Chat history ko sahi syntax se get karen (or ka use galat tha)
    history = cl.user_session.get("Chat_history") or []

    # User ke message ko history mein add karen
    history.append({"role": "user", "content": message.content})

    try:
        # completion call (agar async ho to 'await' karen, yahan assume sync hai)
        response = completion(
            model="openrouter/mistralai/devstral-small:free",
            api_key=OPENROUTER_API_KEY,
            base_url=BASE_URL,
            messages=history
        )

        response_content = response.choices[0].message.content

        # Thinking message update karen actual response se
        msg.content = response_content
        await msg.update()

        # Assistant ke response ko history mein sahi role ke saath add karen
        history.append({"role": "assistant", "content": response_content})

        # Updated history wapas session mein set karen
        cl.user_session.set("Chat_history", history)

        # Console par log karen (optional)
        print(f'User: {message.content}')
        print(f'RSK AI Assistant: {response_content}')

    except Exception as e:
        # Error message user ko bhejen
        msg.content = f'Error: {str(e)}'
        await msg.update()
        print(f'Error: {str(e)}')

@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("Chat_history") or []
    with open("Chat_history.json", "w") as f:
        json.dump(history, f, indent=2)
    print("Chat history saved.")

if __name__ == "__main__":
    print("✅ Chainlit app file is being run directly.")
    print("📢 Start the app using: chainlit run your_file.py")
