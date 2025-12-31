"""GitHub search and code analysis tools."""

from typing import Optional

import requests
from crewai.tools import tool


@tool("github_code_search")
def github_code_search(query: str, language: Optional[str] = None) -> str:
    """
    Search GitHub for code examples.

    Args:
        query: Search query (e.g., "Model Context Protocol")
        language: Programming language filter (e.g., "python", "typescript")

    Returns:
        Formatted search results with repository links and code snippets
    """
    # Build search query
    search_query = query
    if language:
        search_query += f" language:{language}"

    # GitHub Code Search API
    url = "https://api.github.com/search/code"
    params = {
        "q": search_query,
        "sort": "indexed",
        "order": "desc",
        "per_page": 5
    }

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("total_count", 0) == 0:
            return f"No code results found for: {query}"

        # Format results
        results = []
        for item in data.get("items", [])[:5]:
            result = f"""
Repository: {item['repository']['full_name']}
File: {item['name']}
Path: {item['path']}
URL: {item['html_url']}
"""
            results.append(result)

        return "\n---\n".join(results)

    except requests.exceptions.RequestException as e:
        return f"Error searching GitHub: {str(e)}"


@tool("github_repo_search")
def github_repo_search(query: str) -> str:
    """
    Search GitHub for repositories.

    Args:
        query: Search query (e.g., "MCP server")

    Returns:
        Formatted list of repositories with descriptions and stats
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("total_count", 0) == 0:
            return f"No repositories found for: {query}"

        # Format results
        results = []
        for repo in data.get("items", [])[:5]:
            result = f"""
Repository: {repo['full_name']}
Description: {repo.get('description', 'No description')}
Stars: {repo['stargazers_count']} | Forks: {repo['forks_count']}
Language: {repo.get('language', 'N/A')}
URL: {repo['html_url']}
"""
            results.append(result)

        return "\n---\n".join(results)

    except requests.exceptions.RequestException as e:
        return f"Error searching GitHub: {str(e)}"
