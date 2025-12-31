"""Main Crew orchestration for MCP investigation."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from crewai import Crew, Process
from rich.console import Console
from rich.panel import Panel

from .agents.architect import create_architect
from .agents.mcp_researcher import create_mcp_researcher
from .agents.tech_analyst import create_tech_analyst
from .agents.writer import create_technical_writer
from .config import OUTPUT_DIR, VERBOSE
from .tasks.investigation_tasks import (
    create_architecture_design_task,
    create_documentation_task,
    create_mcp_research_task,
    create_technical_analysis_task,
)


class MCPInvestigationCrew:
    """
    Main orchestrator for MCP investigation workflow.

    This crew coordinates 4 agents working sequentially to investigate
    MCP tool architectures and produce comprehensive documentation.
    """

    def __init__(self, verbose: bool = VERBOSE, session_logger=None):
        """
        Initialize the investigation crew.

        Args:
            verbose: Enable verbose logging
            session_logger: Optional SessionLogger instance for detailed logging
        """
        self.verbose = verbose
        self.console = Console()
        self.session_logger = session_logger

        # Create agents
        self.mcp_researcher = create_mcp_researcher()
        self.tech_analyst = create_tech_analyst()
        self.architect = create_architect()
        self.writer = create_technical_writer()

    def investigate(
        self,
        topic: str,
        depth: str = "comprehensive"
    ) -> str:
        """
        Run the MCP investigation workflow.

        Args:
            topic: Investigation topic (e.g., "web scraping MCP tool")
            depth: Investigation depth ("quick", "standard", "comprehensive")

        Returns:
            Final investigation report as markdown string
        """
        self.console.print(Panel.fit(
            f"[bold cyan]MCP Investigation Tool[/bold cyan]\n"
            f"Topic: {topic}\n"
            f"Depth: {depth}",
            border_style="cyan"
        ))

        # Create tasks
        task1 = create_mcp_research_task(self.mcp_researcher, topic)
        if self.session_logger:
            self.session_logger.log_agent_prompt(
                "MCP Researcher",
                task1.description,
                {"task_id": "task1", "expected_output": task1.expected_output}
            )

        task2 = create_technical_analysis_task(
            self.tech_analyst,
            topic,
            context=[task1]
        )
        if self.session_logger:
            self.session_logger.log_agent_prompt(
                "Technical Analyst",
                task2.description,
                {"task_id": "task2", "expected_output": task2.expected_output}
            )

        task3 = create_architecture_design_task(
            self.architect,
            topic,
            context=[task1, task2]
        )
        if self.session_logger:
            self.session_logger.log_agent_prompt(
                "System Architect",
                task3.description,
                {"task_id": "task3", "expected_output": task3.expected_output}
            )

        task4 = create_documentation_task(
            self.writer,
            topic,
            context=[task1, task2, task3]
        )
        if self.session_logger:
            self.session_logger.log_agent_prompt(
                "Technical Writer",
                task4.description,
                {"task_id": "task4", "expected_output": task4.expected_output}
            )

        # Create crew
        crew = Crew(
            agents=[
                self.mcp_researcher,
                self.tech_analyst,
                self.architect,
                self.writer
            ],
            tasks=[task1, task2, task3, task4],
            process=Process.sequential,
            verbose=self.verbose
        )

        # Execute investigation
        self.console.print("\n[yellow]Starting investigation...[/yellow]\n")

        try:
            result = crew.kickoff()

            # Log task outputs if session logger is available
            if self.session_logger:
                # Log each task's output
                for i, task in enumerate([task1, task2, task3, task4], 1):
                    agent_names = ["MCP Researcher", "Technical Analyst", "System Architect", "Technical Writer"]
                    if hasattr(task, 'output') and task.output:
                        self.session_logger.log_agent_output(
                            agent_names[i-1],
                            str(task.output),
                            {"task_id": f"task{i}", "task_name": task.description[:100]}
                        )

                        # Log stage transitions
                        if i < 4:
                            self.session_logger.log_stage_transition(
                                from_stage=agent_names[i-1],
                                to_stage=agent_names[i],
                                data_passed=str(task.output)[:500]
                            )

            # Save output
            output_file = self._save_result(topic, result)

            self.console.print(Panel.fit(
                f"[bold green]Investigation Complete![/bold green]\n"
                f"Report saved to: {output_file}",
                border_style="green"
            ))

            return str(result)

        except Exception as e:
            self.console.print(f"[bold red]Error during investigation:[/bold red] {str(e)}")
            raise

    def _save_result(self, topic: str, result: str) -> Path:
        """
        Save investigation result to file.

        Args:
            topic: Investigation topic
            result: Investigation result

        Returns:
            Path to saved file
        """
        # Create safe filename
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
        safe_topic = safe_topic.strip().replace(' ', '_')[:50]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"investigation_{safe_topic}_{timestamp}.md"

        output_path = OUTPUT_DIR / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(result))

        return output_path
