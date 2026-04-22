import os, json
from dotenv import load_dotenv
from openai import OpenAI

from schemas.llm_response import LLMResponse
from tools.tool_specs import TOOLS
from tools.tool_adapter import to_openai_tools
from tools.extract_requirements import extract_requirements

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-mini"


def call_openai(prompt: str) -> LLMResponse:
    tools = to_openai_tools(TOOLS)

    resp = client.responses.create(
        model=MODEL,
        input=prompt,
        tools=tools
    )

    tool_calls = getattr(resp, "tool_calls", None)

    if tool_calls:
        call = tool_calls[0]

        if call.name == "extract_requirements":
            result = extract_requirements(**call.arguments)

            follow_up = client.responses.create(
                model=MODEL,
                input=[
                    {"role": "user", "content": prompt},
                    {
                        "type": "tool_result",
                        "tool_name": call.name,
                        "content": json.dumps(result)
                    }
                ],
                tools=tools
            )

            return LLMResponse(
                provider="openai",
                model=MODEL,
                input=prompt,
                output=follow_up.output[0].content[0].text,
                request_id=follow_up.id
            )

    return LLMResponse(
        provider="openai",
        model=MODEL,
        input=prompt,
        output=resp.output[0].content[0].text,
        request_id=resp.id
    )