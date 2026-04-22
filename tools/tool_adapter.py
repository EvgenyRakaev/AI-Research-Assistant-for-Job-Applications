def to_openai_tools(tools):
    return [
        {
            "type": "function",
            "name": t["name"],
            "description": t["description"],
            "parameters": t["parameters"]
        }
        for t in tools
    ]


def to_claude_tools(tools):
    return [
        {
            "name": t["name"],
            "description": t["description"],
            "input_schema": t["parameters"]
        }
        for t in tools
    ]


def to_gemini_tools(tools, types):
    return types.Tool(function_declarations=tools)