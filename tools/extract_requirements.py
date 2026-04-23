def extract_requirements(text: str) -> dict:
    # naive: extract hardcoded keywords
    keywords = [
        "python", "react", "aws", "docker", "sql",
        "distributed systems",
        "event-driven",
        "ml",
        "machine learning"
    ]

    return {
        "skills": keywords,
        "summary": f"Found {len(keywords)} skills"
    }