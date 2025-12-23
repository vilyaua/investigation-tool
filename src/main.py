"""Main entry point for the MCP Investigation Tool."""

import sys
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from .crew import MCPInvestigationCrew


def main():
    """Main CLI interface for the investigation tool."""
    console = Console()

    # Print banner
    console.print("""
[bold cyan]╔══════════════════════════════════════════════════╗
║     MCP Investigation Tool - MVP v0.1.0          ║
║     Multi-Agent Research System                  ║
╚══════════════════════════════════════════════════╝[/bold cyan]
""")

    # Check if .env exists
    if not Path(".env").exists():
        console.print("[bold yellow]Warning:[/bold yellow] .env file not found!")
        console.print("Please create a .env file with your OPENAI_API_KEY")
        console.print("See .env.example for template\n")
        sys.exit(1)

    # Get investigation topic from user
    default_topic = "web scraping MCP tool architecture"

    console.print("[bold]Enter investigation topic[/bold]")
    console.print(f"(Press Enter for default: '{default_topic}')")

    topic = Prompt.ask("Topic", default=default_topic)

    # Get depth
    depth = Prompt.ask(
        "Investigation depth",
        choices=["quick", "standard", "comprehensive"],
        default="comprehensive"
    )

    console.print()

    # Run investigation
    try:
        crew = MCPInvestigationCrew(verbose=True)
        crew.investigate(topic=topic, depth=depth)

    except KeyboardInterrupt:
        console.print("\n[yellow]Investigation cancelled by user[/yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
