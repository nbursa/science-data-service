import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def translate_content(content, target_language='Serbian'):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Translate the following content to {target_language}:\n\n{content}",
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        translated_content = response.choices[0].text.strip()
        return translated_content
    except Exception as e:
        print(f"Error during translation: {e}")
        return None
