import os, json
from dotenv import load_dotenv
from anthropic import Anthropic

from schemas.llm_response import LLMResponse
from tools.tool_specs import TOOLS
from tools.tool_adapter import to_claude_tools
from tools.extract_requirements import extract_requirements

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-3-5-sonnet-20241022"


def call_claude(prompt: str) -> LLMResponse:
    tools = to_claude_tools(TOOLS)

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        tools=tools,
        messages=[{"role": "user", "content": prompt}]
    )

    tool_call = None
    for block in response.content:
        if block.type == "tool_use":
            tool_call = block

    if tool_call and tool_call.name == "extract_requirements":
        result = extract_requirements(**tool_call.input)

        final = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": json.dumps(result)
                    }]
                }
            ]
        )

        return LLMResponse(
            provider="claude",
            model=MODEL,
            input=prompt,
            output=final.content[0].text,
            request_id=final.id
        )

    return LLMResponse(
        provider="claude",
        model=MODEL,
        input=prompt,
        output=response.content[0].text,
        request_id=response.id
    )