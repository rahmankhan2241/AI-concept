import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization" : f"Bearer {api_key}",
    "Content-Type": "application/json"
}

system_role = input("Please mention the role for the system: ")
context_window_length = int(input("How many previous chats, you want him to remember (example 5): " ))
conversation = [{"role": "system", "content": system_role}]

while True:
    user = input("\nuser: ")
    if user.lower() in ['exit', 'quit']:
        break

    conversation.append({"role": "user", "content": user})

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages" : conversation[0:1] + conversation[-context_window_length:]
    }

    try:
        response = requests.post(url, headers = headers, json = body)
        
        if response.status_code == 200:
            ai_response = response.json()["choices"][0]["message"]["content"]
            conversation.append({
                "role" : "assistant",
                "content" : ai_response
            })
            print(f"AI: {ai_response}")
            
        elif response.status_code == 429:
            ## Checking for rate limits
            print("AI: Ohh, seems my limits has crossed, using free version no 😢")
            # removing from the conversation since it should not come
            conversation.pop()
            
        else:

            print(f"AI: Try again, maybe it's an AI fault. (Status Code: {response.status_code})")
            conversation.pop()

    except Exception as e:
        print("AI: Try again, maybe it's an AI fault or network issue.")
        if 'conversation' in locals() and len(conversation) > 1:
            conversation.pop()