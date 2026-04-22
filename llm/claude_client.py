import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic, RateLimitError

from schemas.llm_response import LLMResponse

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-3-5-sonnet-20241022"


def call_claude(prompt: str) -> LLMResponse:
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # ⚠️ структура другая, не как OpenAI
        output_text = response.content[0].text

        return LLMResponse(
            provider="claude",
            model=MODEL,
            input=prompt,
            output=output_text,
            request_id=response.id
        )


    except RateLimitError as e:
        raise Exception(json.dumps({
            "error": "quota_exceeded",
            "provider": "claude",
            "model": MODEL,
            "raw": str(e)
        }))


    except Exception as e:
        raise Exception(json.dumps({
            "error": "provider_failed",
            "provider": "claude",
            "model": MODEL,
            "raw": str(e)
        }))