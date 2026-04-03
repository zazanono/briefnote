import os
from typing import List

import httpx

TAVILY_BASE = os.getenv('TAVILY_BASE_URL', 'https://api.tavily.com')
TAVILY_KEY = os.getenv('TAVILY_API_KEY', '')


def search(query: str, limit: int = 3) -> List[dict]:
    """Perform a simple Tavily web search. Returns a list of results with keys: title, url, snippet, host."""
    if not TAVILY_KEY:
        raise RuntimeError('TAVILY_API_KEY not set')

    url = f"{TAVILY_BASE}/v1/search"
    headers = {
        'Authorization': f'Bearer {TAVILY_KEY}',
        'Content-Type': 'application/json',
    }
    body = { 'q': query, 'limit': limit }
    try:
        resp = httpx.post(url, json=body, headers=headers, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        items = data.get('results') or data.get('items') or []
        out = []
        for it in items[:limit]:
            title = it.get('title') or it.get('name') or ''
            link = it.get('url') or it.get('link') or ''
            snippet = it.get('snippet') or it.get('excerpt') or ''
            host = ''
            try:
                from urllib.parse import urlparse
                host = urlparse(link).hostname or ''
            except Exception:
                host = ''
            out.append({ 'title': title, 'url': link, 'snippet': snippet, 'host': host })
        return out
    except Exception as e:
        raise RuntimeError(f'Tavily search failed: {e}')
