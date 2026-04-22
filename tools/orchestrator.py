# tools/orchestrator.py

from llm.openai_client import call_openai
from llm.gemini_client import call_gemini
from llm.claude_client import call_claude
from llm.groq_client import call_groq

from datetime import datetime

CLIENTS = {
    "openai": call_openai,
    "gemini": call_gemini,
    "claude": call_claude,
    "groq": call_groq
}

def run_llm(provider: str, prompt: str):
    provider = provider.lower()

    if provider not in CLIENTS:
        msg = f"{provider} not supported"
        print(f"[{datetime.now()}][{provider.upper()}][invalid] {msg}")
        raise ValueError(msg)

    try:
        result = CLIENTS[provider](prompt)

        # лог успеха (по желанию можно убрать)
        print(f"[{datetime.now()}][{provider.upper()}][ok]")

        return result

    except Exception as e:
        raw = str(e)

        # короткий лог ошибки
        print(f"[{datetime.now()}][{provider.upper()}][error] {raw[:500]}")

        raise