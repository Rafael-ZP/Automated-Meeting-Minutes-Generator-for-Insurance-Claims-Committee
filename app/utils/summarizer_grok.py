import os
import requests
from models.groq_prompt import GEMINI_PROMPT_TEMPLATE

def generate_mom(transcript: str, participants: list = None):
    xai_api_key = os.getenv("XAI_API_KEY")  # Store your Grok API key as XAI_API_KEY
    if not xai_api_key:
        raise ValueError("Missing XAI_API_KEY in environment variables.")

    prompt = GEMINI_PROMPT_TEMPLATE.format(transcript=transcript)
    headers = {
        "Authorization": f"Bearer {xai_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-4",  # Options: grok-3, grok-3-mini, grok-4, etc.
        "messages": [
            {"role": "system", "content": "You are an assistant that summarizes transcripts into minutes of meeting (MoM)."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Grok API error {response.status_code}: {response.text}")

    return response.json()['choices'][0]['message']['content']