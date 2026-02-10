import chainlit as cl
from openai import AsyncOpenAI

# Connects to your local Ollama
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Chatbot settings
settings = {
    "model": "llama3.2", # Make sure this matches your installed model (llama3 or llama3.2)
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start
def start_chat():
    # --- THIS IS WHERE YOU DEFINE THE CHARACTER ---
    system_instruction = """
    You are 'RecruitBot', the official AI assistant for SmartRecruit.
    
    Your goal is to help:
    1. Candidates find jobs (tell them to check the 'Find Jobs' page).
    2. Employers post jobs (tell them to login to the HR Dashboard).
    
    Guidelines:
    - Be professional, encouraging, and brief.
    - If asked about salary, say "Salaries vary by role, please check specific job listings."
    - Do NOT talk about laptop repair or unrelated topics.
    - Always end answers with a helpful tone.
    """
    
    # Initialize session history with this new persona
    cl.user_session.set("message_history", [{"role": "system", "content": system_instruction}])

@cl.on_message
async def main(message: cl.Message):
    # Get history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    try:
        stream = await client.chat.completions.create(
            messages=message_history, 
            stream=True, 
            **settings
        )

        async for part in stream:
            if token := part.choices[0].delta.content:
                await msg.stream_token(token)

        message_history.append({"role": "assistant", "content": msg.content})
        await msg.update()

    except Exception as e:
        await cl.Message(content=f"Error: Make sure Ollama is running! ({str(e)})").send()