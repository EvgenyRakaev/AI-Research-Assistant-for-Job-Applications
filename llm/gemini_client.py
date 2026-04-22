import os
from dotenv import load_dotenv
from google import genai

from schemas.llm_response import LLMResponse

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"


def call_gemini(prompt: str) -> LLMResponse:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    output_text = response.text

    return LLMResponse(
        provider="gemini",
        model=MODEL,
        input=prompt,
        output=output_text,
        request_id=None
    )