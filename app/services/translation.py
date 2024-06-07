import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def translate_content(content: str) -> str:
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Translate the following text to Serbian: {content}",
        max_tokens=1000
    )
    return response.choices[0].text.strip()
