import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def translate_content(content, target_language='sr'):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following text to {target_language}: {content}",
        max_tokens=1000
    )
    return response.choices[0].text.strip()
