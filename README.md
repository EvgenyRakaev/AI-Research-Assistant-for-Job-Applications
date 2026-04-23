# AI Research Assistant for Job Applications

A lightweight backend service that analyzes job descriptions and helps extract useful information for job applications.

## What it does

- Accepts a job description as input
- Routes the request to different LLM providers (OpenAI, Claude, Gemini, Groq)
- Supports basic tool/function calling (e.g. extracting required skills)
- Returns structured responses that can be used for further automation

## Why this project

The goal of this project is to explore how different LLM providers can be integrated behind a single API.

Each provider has a different way of handling tool/function calling, so this project focuses on:
- normalizing tool definitions
- handling provider-specific APIs
- building a simple multi-step interaction loop (LLM → tool → response)

## Architecture (high level)

- **FastAPI** — main API layer
- **/ai/{provider} endpoint** — routes requests to selected LLM provider
- **llm/** — provider-specific clients (OpenAI, Claude, Gemini, Groq)
- **tools/** — backend functions callable by LLMs
- **tool adapter** — normalizes tool schemas across providers
- **orchestrator** — controls request flow and tool execution

## Example flow

1. Client sends job description
2. LLM decides to call a tool (e.g. extract_requirements)
3. Backend executes Python function
4. Result is sent back to LLM
5. Final response is returned to client

## Running locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload