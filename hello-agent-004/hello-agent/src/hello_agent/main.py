import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load .env variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("Api_Key")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not valid or missing.")

external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

model = OpenAIChatCompletionsModel(
    model='microsoft/mai-ds-r1:free',  
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(
    name="Assistant",
    instructions="you are a translator.",
    model=model
)

result = Runner.run_sync(agent, "my name is waniya shah", run_config=config)

print("\nAgent Is Responding\n")
print(result.final_output)