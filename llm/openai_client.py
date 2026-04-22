from openai import OpenAI, RateLimitError
from schemas.llm_response import LLMResponse
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-mini"

def call_openai(prompt: str) -> LLMResponse:
    try:
        response = client.responses.create(
            model=MODEL,
            input=prompt
        )

        output_text = response.output[0].content[0].text

        return LLMResponse(
            provider="openai",
            model=MODEL,
            input=prompt,
            output=output_text,
            request_id=response.id,
        )


    except RateLimitError as e:
        raise Exception(json.dumps({
            "error": "quota_exceeded",
            "provider": "openai",
            "model": MODEL,
            "raw": str(e)
        }))

    except Exception as e:
        raise Exception(json.dumps({
            "error": "provider_failed",
            "provider": "openai",
            "model": MODEL,
            "raw": str(e)
        }))