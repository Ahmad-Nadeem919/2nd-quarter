import asyncio
import chainlit as cl
import litellm
import os
from dotenv import load_dotenv

load_dotenv()
litellm.api_key = os.getenv("GEMINI_API_KEY")

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(" Welcome to chainlit! Ask me anything.").send()
    cl.user_session.set("chat_history", [])

@cl.on_message
async def on_message(message: cl.Message):
    chat_history = cl.user_session.get("chat_history") or []
    chat_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    try:
        # Call Gemini (full response)
        response = litellm.completion(
            model="gemini/gemini-1.5-flash",
            messages=chat_history
        )
        full_reply = response["choices"][0]["message"]["content"]

        # Simulate streaming by chunking reply text
        chunk_size = 30  # characters per chunk, adjust as needed
        for i in range(0, len(full_reply), chunk_size):
            chunk = full_reply[i : i + chunk_size]
            await msg.stream_token(chunk)
            await asyncio.sleep(0.1)  # simulate delay for streaming effect

        # Finalize message
        await msg.update()

        # Update chat history
        chat_history.append({"role": "assistant", "content": full_reply})
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        await msg.update(content=f"❌ Error: {str(e)}")

@cl.on_chat_end
def on_chat_end():
    chat_history = cl.user_session.get("chat_history") or []
    with open("chat_history.json", "a") as f:
        import json
        json.dump(chat_history, f, indent=4)
