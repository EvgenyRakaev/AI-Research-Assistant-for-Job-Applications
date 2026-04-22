## FastAPI endpoint /analyze
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")






from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input="Write a short bedtime story about a unicorn. max 100 words"
)

print(response.output_text)
