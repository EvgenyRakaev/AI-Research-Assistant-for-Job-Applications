import os
from dotenv import load_dotenv
from groq import Groq

from schemas.llm_response import LLMResponse
from tools.extract_requirements import extract_requirements

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


SYSTEM_PROMPT = """
You are an AI agent.

If the user asks to extract skills or requirements,
respond ONLY in JSON:

{
  "tool": "extract_requirements",
  "args": {
    "text": "..."
  }
}

Otherwise respond normally.
"""


def call_groq(prompt: str) -> LLMResponse:
    print("\n=== GROQ CALL ===")
    print("PROMPT:", prompt)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    print("\n=== RAW LLM RESPONSE ===")
    print(content)

    # --- attempt to parse as tool call ---
    import json

    try:
        data = json.loads(content)

        if data.get("tool") == "extract_requirements":
            print("\n=== TOOL CALL DETECTED (MANUAL) ===")

            result = extract_requirements(**data["args"])

            print("\n=== TOOL RESULT ===")
            print(result)

            return LLMResponse(
                provider="groq",
                model=MODEL,
                input=prompt,
                output=str(result),
                request_id=response.id
            )

    except Exception:
        pass

    # --- regular response ---
    return LLMResponse(
        provider="groq",
        model=MODEL,
        input=prompt,
        output=content,
        request_id=response.id
    )