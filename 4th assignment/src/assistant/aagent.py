import chainlit as cl
import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')

# OpenAI client for Gemini
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define a simple function tool
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

# Define agent
agent = Agent(
    name="Assistant",
    instructions="You are an assistant.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)

# Chainlit: Chat start
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(content="Hello! How can I assist you today?").send()

# Chainlit: On message
@cl.on_message
async def on_message(message: cl.Message):
    chat_history = cl.user_session.get("chat_history")
    query = message.content

    result = await Runner.run(agent, query)

    chat_history.append({"role": "user", "message": query})
    chat_history.append({"role": "assistant", "message": result.final_output})
    cl.user_session.set("chat_history", chat_history)



    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f, indent=4)
    await cl.Message(content=result.final_output).send()
