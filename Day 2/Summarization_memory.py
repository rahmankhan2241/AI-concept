## As of now context Window based LLM has the memory so to remember the overall summarization of the chat we will use Summarization technique

import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization" : f"Bearer {api_key}", "Content-Type": "application/json"}

context_window_length = 4

conversation_history = []

while True:
    user_input = input("user: ").strip()
    if len(conversation_history) > context_window_length:
        user_input = user_input + "Please remember all the core details of the conversation in a summary"
        print(user_input)
        conversation_history.append({"role": "user", "content": user_input})
    
    conversation_history.append({"role": "user", "content": user_input})

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": conversation_history[-context_window_length:]
    }

    try:
        response = requests.post(url, headers = headers, json = body)
        if response.status_code == 200:
            ai_response = ai_response = response.json()["choices"][0]["message"]["content"]
            print(ai_response)
            conversation_history.append({"role": "assistant", "content": ai_response})
        elif response.status_code == 429:
            print("Ohhh seems ! The AIs limit has crossed, Poor people does'nt have paid api 😢")
        
    except Exception as e:
        print("AI: Try again, maybe it's an AI fault or network issue.")


    
    
