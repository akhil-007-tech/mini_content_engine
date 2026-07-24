from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def generate_prompt(product_name, description):
    prompt = f"""
You are an expert advertising prompt engineer.

Generate one highly detailed AI image generation prompt.

Product:
{product_name}

Description:
{description}

The output should contain ONLY the final prompt.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()