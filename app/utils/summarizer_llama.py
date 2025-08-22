from groq import Groq
import os
from models.groq_prompt import GROQ_PROMPT_TEMPLATE

def generate_mom(transcript: str, participants: list = None):
    prompt = GROQ_PROMPT_TEMPLATE.format(transcript=transcript)

    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes transcripts into minutes of meeting (MoM)."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=1024,
    )

    return response.choices[0].message.content