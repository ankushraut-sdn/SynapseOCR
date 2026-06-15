import requests
import json
from app.config import GEMINI_API_KEY

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"


def organize_text(transcribed_text: str) -> str:
    prompt = f"""
    You will be given raw text extracted using OCR from a document.

    Your task is to clean and format this text into a well-organized and readable format. Do not create or infer any new content. Simply organize the existing content using proper spacing, punctuation, and line breaks where necessary.

    ---
    {transcribed_text}
    ---
    Return only the cleaned and formatted text.
    """

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    result = response.json()
    soap_notes = result["candidates"][0]["content"]["parts"][0]["text"]
    return soap_notes
