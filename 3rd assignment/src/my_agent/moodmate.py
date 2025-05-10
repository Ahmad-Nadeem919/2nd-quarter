import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is set
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="""    You are MoodMate, a friendly and emotionally intelligent assistant.
    Your job is to help users reflect on their emotions and offer general tips for self-care.
    Be supportive, non-judgmental, and never offer medical advice.
    Use soft, comforting language and speak like a calm friend or life coach.
    Always end your response with a gentle question to encourage continued reflection.""", model=model)

promt=input("enter your promt here:-")
result = Runner.run_sync(agent, promt, run_config=config)

print("\nCALLING AGENT\n")
print(result.final_output)
with open("output.md", "a") as f:
    f.write("#  Agent Response\n\n")
    f.write(result.final_output)
