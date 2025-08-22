from models.groq_prompt import GEMINI_PROMPT_TEMPLATE
import os

def generate_mom(transcript:str, participants:list=None):
    import google.generativeai as genai
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=gemini_api_key)
    prompt = GEMINI_PROMPT_TEMPLATE.format(transcript=transcript)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
