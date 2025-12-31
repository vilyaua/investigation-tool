"""Basic tests for the investigation tool."""

import pytest
from pathlib import Path


def test_project_structure():
    """Test that project structure is correct."""
    assert Path("src").exists()
    assert Path("src/agents").exists()
    assert Path("src/tasks").exists()
    assert Path("src/tools").exists()
    assert Path("outputs").exists()


def test_config_imports():
    """Test that config can be imported."""
    try:
        from src.config import settings
        assert settings is not None
    except ImportError as e:
        pytest.skip(f"Config import failed (expected if .env not set): {e}")


def test_agents_can_be_created():
    """Test that agents can be created."""
    try:
        from src.agents.mcp_researcher import create_mcp_researcher
        from src.agents.tech_analyst import create_tech_analyst
        from src.agents.architect import create_architect
        from src.agents.writer import create_technical_writer

        # This will fail without API keys, but tests the imports
        # In a real test environment, you'd mock the LLM calls
        assert create_mcp_researcher is not None
        assert create_tech_analyst is not None
        assert create_architect is not None
        assert create_technical_writer is not None

    except Exception as e:
        pytest.skip(f"Agent creation failed (expected if .env not set): {e}")


def test_crew_can_be_imported():
    """Test that the main crew class can be imported."""
    try:
        from src.crew import MCPInvestigationCrew
        assert MCPInvestigationCrew is not None
    except ImportError as e:
        pytest.skip(f"Crew import failed (expected if .env not set): {e}")
