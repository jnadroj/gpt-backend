from openai import OpenAI
from app.config.settings import Config

openai_api_key = Config.OPENAI_API_KEY
client = OpenAI()

def get_openai_response(message):
    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": message}],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        print("Error:", e)
