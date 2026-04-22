# tools/tool_specs.py

TOOLS = [
    {
        "name": "extract_requirements",
        "description": "Extract key skills from job description text",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"]
        }
    }
]