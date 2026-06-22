import requests
import os
from dotenv import load_dotenv
import torch.nn.functional as F
import torch
import numpy as np

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

url = (
    f"https://generativelanguage.googleapis.com/"
    f"v1beta/models/gemini-embedding-001:embedContent"
    f"?key={api_key}"
)



user_text = input("Enter your paragraph about what you later need to find answers: ")

documents = []

for para in user_text.split("."):
    if para:
        documents.append(para.strip())
print(documents)


## Code for creating the embedding document
def create_embedding(text):
    body = {
    "model": "models/gemini-embedding-001",
    "content": {
        "parts": [
            {
                "text": text
            }
        ]
    }
}
    try:
        response = requests.post(url, json = body)
        return response.json()["embedding"]["values"]
    except Exception as e:
        return "Some Error Occured"


embedded_senteces = []
for sentence in documents:
    embedded = create_embedding(sentence)
    embedded_senteces.append(embedded)

while True:
    user_query = input("Enter you query: ")

    embedded_query = torch.tensor(create_embedding(user_query)).unsqueeze(0)

    mathing_score = []

    for embedded_sentence in embedded_senteces:
        embedded_doc = torch.tensor(embedded_sentence).unsqueeze(0)

        score = F.cosine_similarity(embedded_query, embedded_doc)
        mathing_score.append(score)

    max_score = np.argmax(mathing_score)
    print(documents[max_score])

        



