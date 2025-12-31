"""MCP Research Agent - Specialized in gathering MCP protocol information."""

from crewai import Agent, LLM

from ..config import RESEARCH_MODEL
from ..tools.web_search import web_search_tool


def create_mcp_researcher() -> Agent:
    """
    Create the MCP Research Agent.

    This agent specializes in gathering information about the Model Context Protocol,
    its tools, patterns, and best practices.

    Returns:
        Configured Agent instance
    """
    llm = LLM(model=RESEARCH_MODEL)

    return Agent(
        role="MCP Protocol Researcher",
        goal="Gather comprehensive and accurate information about MCP (Model Context Protocol) "
             "tools, patterns, implementations, and best practices",
        backstory="""You are an expert researcher specializing in the Model Context Protocol (MCP).
        You have deep knowledge of how MCP works, its architecture, and the ecosystem of tools built around it.
        You excel at finding official documentation, community resources, and real-world implementations.
        You always cite your sources and distinguish between official specs and community practices.""",
        tools=[web_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
