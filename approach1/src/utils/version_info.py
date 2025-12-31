"""Version information for MCP Investigation Tool."""

import subprocess
from typing import Dict
from pathlib import Path


def get_agent_versions() -> Dict[str, str]:
    """Get version information for all agents and dependencies."""
    # Import config to get model information
    try:
        from ..config import RESEARCH_MODEL, ANALYSIS_MODEL
    except ImportError:
        RESEARCH_MODEL = "gpt-4o-mini"
        ANALYSIS_MODEL = "gpt-4o"

    versions = {
        "app_version": "1.1.0",
        "agents": {
            "mcp_researcher": {
                "version": "1.0.0",
                "model": RESEARCH_MODEL
            },
            "tech_analyst": {
                "version": "1.0.0",
                "model": RESEARCH_MODEL
            },
            "architect": {
                "version": "1.0.0",
                "model": ANALYSIS_MODEL
            },
            "technical_writer": {
                "version": "1.0.0",
                "model": ANALYSIS_MODEL
            }
        },
        "dependencies": {}
    }

    # Get installed package versions
    try:
        import crewai
        versions["dependencies"]["crewai"] = crewai.__version__
    except (ImportError, AttributeError):
        versions["dependencies"]["crewai"] = "unknown"

    try:
        import openai
        versions["dependencies"]["openai"] = openai.__version__
    except (ImportError, AttributeError):
        versions["dependencies"]["openai"] = "unknown"

    try:
        import gradio
        versions["dependencies"]["gradio"] = gradio.__version__
    except (ImportError, AttributeError):
        versions["dependencies"]["gradio"] = "unknown"

    # Get Git commit if available
    try:
        git_commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=Path(__file__).parent.parent.parent,
            stderr=subprocess.DEVNULL
        ).decode().strip()
        versions["git_commit"] = git_commit
    except (subprocess.CalledProcessError, FileNotFoundError):
        versions["git_commit"] = "not-available"

    return versions


def format_version_info() -> str:
    """Format version information for display."""
    versions = get_agent_versions()

    info = f"""### 🔧 System Information

**App Version:** {versions['app_version']}
**Git Commit:** {versions.get('git_commit', 'N/A')}

**AI Models:**
- MCP Researcher: {versions['agents']['mcp_researcher']['model']}
- Technical Analyst: {versions['agents']['tech_analyst']['model']}
- System Architect: {versions['agents']['architect']['model']}
- Technical Writer: {versions['agents']['technical_writer']['model']}

**Dependencies:**
- CrewAI: {versions['dependencies'].get('crewai', 'unknown')}
- OpenAI: {versions['dependencies'].get('openai', 'unknown')}
- Gradio: {versions['dependencies'].get('gradio', 'unknown')}
"""
    return info
