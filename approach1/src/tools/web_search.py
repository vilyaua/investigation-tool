"""Web search tools for agents."""

import os
from crewai.tools import tool


@tool("web_search")
def web_search_tool(query: str) -> str:
    """
    Search the web for information using Serper API (falls back to DuckDuckGo).

    Args:
        query: Search query string

    Returns:
        Search results as formatted text
    """
    # Try Serper first if API key is available
    serper_key = os.getenv("SERPER_API_KEY")

    if serper_key:
        try:
            import requests

            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": serper_key,
                "Content-Type": "application/json"
            }
            data = {"q": query}

            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            results = response.json()

            if "organic" in results and results["organic"]:
                formatted = []
                for r in results["organic"][:5]:
                    formatted.append(f"Title: {r.get('title', 'N/A')}\n"
                                   f"Link: {r.get('link', 'N/A')}\n"
                                   f"Snippet: {r.get('snippet', 'N/A')}\n")
                return "\n---\n".join(formatted)
        except Exception as e:
            # Fall back to DuckDuckGo
            pass

    # Fallback to DuckDuckGo
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return f"No results found for: {query}"

        formatted = []
        for r in results:
            formatted.append(f"Title: {r.get('title', 'N/A')}\n"
                           f"Link: {r.get('href', 'N/A')}\n"
                           f"Snippet: {r.get('body', 'N/A')}\n")

        return "\n---\n".join(formatted)

    except Exception as e:
        return f"Search error: {str(e)}"
