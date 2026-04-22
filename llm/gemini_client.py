import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from schemas.llm_response import LLMResponse
from tools.tool_specs import TOOLS
from tools.tool_adapter import to_gemini_tools
from tools.extract_requirements import extract_requirements

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"


def call_gemini(prompt: str) -> LLMResponse:
    tools = to_gemini_tools(TOOLS, types)
    config = types.GenerateContentConfig(tools=[tools])

    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt],
        config=config
    )

    tool_call = None
    for p in response.candidates[0].content.parts:
        if getattr(p, "function_call", None):
            tool_call = p.function_call

    if tool_call and tool_call.name == "extract_requirements":
        result = extract_requirements(**tool_call.args)

        contents = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
            response.candidates[0].content,
            types.Content(
                role="user",
                parts=[
                    types.Part.from_function_response(
                        name=tool_call.name,
                        response={"result": result}
                    )
                ]
            )
        ]

        final = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config
        )

        return LLMResponse(
            provider="gemini",
            model=MODEL,
            input=prompt,
            output=final.text,
            request_id=None
        )

    return LLMResponse(
        provider="gemini",
        model=MODEL,
        input=prompt,
        output=response.text,
        request_id=None
    )