import os
from dotenv import load_dotenv
from groq import Groq

from schemas.llm_response import LLMResponse

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


def call_groq(prompt: str) -> LLMResponse:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # ⚠️ как у старого OpenAI Chat API
    output_text = response.choices[0].message.content

    return LLMResponse(
        provider="groq",
        model=MODEL,
        input=prompt,
        output=output_text,
        request_id=getattr(response, "id", None)
    )