import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("FIREWORKS_API_KEY")

url = "https://api.fireworks.ai/inference/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "accounts/fireworks/models/glm-5p2",
    "messages": [{"role": "user", "content": "Say hello in one sentence."}]
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.json())