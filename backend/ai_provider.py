import os
from typing import Iterator

import httpx

BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "qwen/qwen3.6-plus:free")
API_KEY = os.getenv("OPENROUTER_API_KEY", "")


def stream_chat(messages: list[dict], model: str | None = None) -> Iterator[str]:
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-OpenRouter-Title": "BriefNote",
    }
    # OpenRouter doesn't support streaming in our usage; request non-streaming
    body = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "stream": False,
    }

    # increase timeout to allow longer responses
    resp = httpx.post(f"{BASE_URL}/chat/completions", json=body, headers=headers, timeout=120.0)
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text}")

    data = resp.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

    if not content:
        return

    # Yield in small chunks so the frontend can display progressive typing
    for i in range(0, len(content), 8):
        yield content[i : i + 8]
