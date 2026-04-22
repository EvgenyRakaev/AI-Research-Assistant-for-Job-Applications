# schemas/llm_response.py
from pydantic import BaseModel
from typing import Optional

class LLMResponse(BaseModel):
    provider: str
    model: str
    input: str
    output: str
    error: Optional[str] = None
    request_id: Optional[str] = None