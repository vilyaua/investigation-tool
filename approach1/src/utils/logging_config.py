"""Logging configuration with session tracking for MCP Investigation Tool."""

import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import json


class SessionLogger:
    """Logger with session ID tracking for detailed flow analysis."""

    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize session logger.

        Args:
            session_id: Optional session ID, generates new one if not provided
        """
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.start_time = datetime.now()

        # Create logs directory
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)

        # Setup logger
        self.logger = logging.getLogger(f"mcp_investigation.{self.session_id}")
        self.logger.setLevel(logging.DEBUG)

        # File handler for this session
        log_file = self.logs_dir / f"session_{self.session_id}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            f'[%(asctime)s] [SESSION:{self.session_id}] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        self.log_file = log_file
        self.events = []

    def log_event(self, event_type: str, message: str, **kwargs):
        """
        Log an event with metadata.

        Args:
            event_type: Type of event (e.g., 'investigation_start', 'agent_task', etc.)
            message: Event message
            **kwargs: Additional metadata
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "message": message,
            **kwargs
        }
        self.events.append(event)

        # Log to file with structured data
        self.logger.info(f"{event_type.upper()}: {message} | Metadata: {json.dumps(kwargs)}")

    def start_investigation(self, topic: str, depth: str):
        """Log investigation start."""
        self.log_event(
            "investigation_start",
            f"Starting investigation: {topic}",
            topic=topic,
            depth=depth
        )

    def start_phase(self, phase_num: int, phase_name: str):
        """Log phase start."""
        self.log_event(
            "phase_start",
            f"Phase {phase_num}/4: {phase_name}",
            phase=phase_num,
            phase_name=phase_name
        )

    def log_agent_action(self, agent_name: str, action: str, details: Optional[dict] = None):
        """Log agent action."""
        self.log_event(
            "agent_action",
            f"Agent '{agent_name}': {action}",
            agent=agent_name,
            action=action,
            details=details or {}
        )

    def log_agent_prompt(self, agent_name: str, prompt: str, metadata: Optional[dict] = None):
        """Log the full prompt sent to an agent."""
        self.log_event(
            "agent_prompt",
            f"Prompt sent to {agent_name}",
            agent=agent_name,
            prompt=prompt,
            prompt_length=len(prompt),
            **(metadata or {})
        )

    def log_agent_output(self, agent_name: str, output: str, metadata: Optional[dict] = None):
        """Log the full output from an agent."""
        self.log_event(
            "agent_output",
            f"Output received from {agent_name}",
            agent=agent_name,
            output=output,
            output_length=len(output),
            **(metadata or {})
        )

    def log_stage_transition(self, from_stage: str, to_stage: str, data_passed: Optional[str] = None):
        """Log transition between stages with data passed."""
        self.log_event(
            "stage_transition",
            f"Transitioning from {from_stage} to {to_stage}",
            from_stage=from_stage,
            to_stage=to_stage,
            data_passed=data_passed,
            data_length=len(data_passed) if data_passed else 0
        )

    def log_tool_use(self, tool_name: str, query: str, result_summary: str):
        """Log tool usage."""
        self.log_event(
            "tool_use",
            f"Tool '{tool_name}' executed",
            tool=tool_name,
            query=query,
            result_summary=result_summary
        )

    def complete_investigation(self, success: bool, output_file: Optional[str] = None):
        """Log investigation completion."""
        duration = (datetime.now() - self.start_time).total_seconds()
        self.log_event(
            "investigation_complete",
            "Investigation completed" if success else "Investigation failed",
            success=success,
            duration_seconds=duration,
            output_file=output_file
        )

    def get_session_summary(self) -> dict:
        """Get summary of session."""
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "events_count": len(self.events),
            "log_file": str(self.log_file)
        }

    def export_session_log(self) -> Path:
        """Export session events as JSON."""
        json_file = self.logs_dir / f"session_{self.session_id}_events.json"
        with open(json_file, 'w') as f:
            json.dump({
                "session_summary": self.get_session_summary(),
                "events": self.events
            }, f, indent=2)
        return json_file
