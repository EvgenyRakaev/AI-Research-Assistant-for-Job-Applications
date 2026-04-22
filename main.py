from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.orchestrator import run_llm
import json

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ai/{llm}")
def ai(llm: str, body: PromptRequest):
    try:
        return run_llm(llm, body.prompt)


    except Exception as e:
        try:
            data = json.loads(str(e))
        except:
            data = {
                "error": "unknown",
                "raw": str(e),
                "provider": llm
            }

        if data.get("error") == "quota_exceeded":
            raise HTTPException(status_code=402, detail=data)
        raise HTTPException(status_code=502, detail=data)