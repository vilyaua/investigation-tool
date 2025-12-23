"""Configuration management for the MCP Investigation Tool."""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # API Keys
    openai_api_key: str
    serper_api_key: Optional[str] = None

    # Model Configuration
    default_research_model: str = "gpt-4o-mini"
    default_analysis_model: str = "gpt-4o"

    # Output Settings
    output_dir: Path = Path("outputs")

    # Agent Configuration
    max_iterations: int = 5
    verbose: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def has_serper(self) -> bool:
        """Check if Serper API key is configured."""
        return bool(self.serper_api_key)


# Global settings instance
settings = Settings()


# Export commonly used values
OPENAI_API_KEY = settings.openai_api_key
RESEARCH_MODEL = settings.default_research_model
ANALYSIS_MODEL = settings.default_analysis_model
OUTPUT_DIR = settings.output_dir
VERBOSE = settings.verbose
