import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, function_tool, Runner
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()

API_KEY = os.getenv("Gemini_Api_Key")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "openrouter/meta-llama/llama-3.3-8b-instruct:free"

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is bright and calm."

# Initialize the Agent with model and tools
weather_agent = Agent(
    name="Weather Bot",
    instructions="You only respond in haikus.",
    model=LitellmModel(
        model=MODEL_NAME,
        base_url=BASE_URL,
        api_key=API_KEY
    ),
    tools=[get_weather]
)

@cl.on_chat_start
async def on_chat_start():
    welcome_message = "🌤️ Welcome to the Weather Bot! Ask me anything..."
    await cl.Message(content=welcome_message).send()

@cl.on_message
async def handle_message(message: cl.Message):
    loading_message = cl.Message(content="🔍 Searching...")
    await loading_message.send()
    try:
        response = await Runner.run(weather_agent, message.content)
        loading_message.content = response.final_output
    except Exception as error:
        loading_message.content = f"Error: {error}"
    await loading_message.update()
