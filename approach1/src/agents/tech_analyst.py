"""Technical Research Agent - Analyzes code examples and implementation patterns."""

from crewai import Agent, LLM

from ..config import RESEARCH_MODEL
from ..tools.github_search import github_code_search, github_repo_search


def create_tech_analyst() -> Agent:
    """
    Create the Technical Research Agent.

    This agent specializes in analyzing code examples, implementation patterns,
    and technical details of MCP tools.

    Returns:
        Configured Agent instance
    """
    llm = LLM(model=RESEARCH_MODEL)

    return Agent(
        role="Code Analyst and Technical Researcher",
        goal="Analyze MCP code examples, identify implementation patterns, "
             "and extract technical insights from real-world projects",
        backstory="""You are a senior software engineer with expertise in analyzing codebases
        and identifying architectural patterns. You have a keen eye for code quality, design patterns,
        and best practices. You excel at reading code from GitHub repositories and extracting
        valuable insights about implementation strategies, common pitfalls, and effective patterns.
        You focus on practical, production-ready code rather than toy examples.""",
        tools=[github_code_search, github_repo_search],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
