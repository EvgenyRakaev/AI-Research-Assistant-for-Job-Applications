# AI-Research-Assistant-for-Job-Applications

## Минимальный дизайн компонентов
### main.py
* FastAPI endpoint /analyze
### schemas/inputs.py
* JobRequest
* ResumeRequest
### tools/*
* обычные Python функции
### llm/openai_client.py
* обёртка над OpenAI Responses API
### services/orchestrator.py
* решает, когда звать модель
* когда исполнять tools
* как собрать финальный JSON

```
app/
  main.py
  llm/
    openai_client.py
    anthropic_client.py
    gemini_client.py
  tools/
    extract_requirements.py
    match_resume.py
    generate_bullets.py
  schemas/
    inputs.py
    outputs.py
  services/
    orchestrator.py
```

