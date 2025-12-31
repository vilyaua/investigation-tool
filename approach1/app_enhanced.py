#!/usr/bin/env python3
"""
Enhanced Gradio Web UI for MCP Investigation Tool
Features: Session logging, version display, real-time progress, proper markdown rendering
"""

import gradio as gr
from datetime import datetime
from pathlib import Path
import markdown

from src.crew import MCPInvestigationCrew
from src.utils.logging_config import SessionLogger
from src.utils.version_info import get_agent_versions, format_version_info


def investigate_topic(topic: str, depth: str):
    """
    Run an investigation with session logging and progress updates.

    Args:
        topic: Investigation topic
        depth: Investigation depth

    Yields:
        Tuple of (report_html, status_message, session_info)
    """
    if not topic or not topic.strip():
        yield "❌ Please enter a topic to investigate.", "Error: No topic provided", ""
        return

    # Initialize session logger
    session_logger = SessionLogger()
    session_id = session_logger.session_id

    try:
        start_time = datetime.now()
        session_logger.start_investigation(topic, depth)

        # Get version info
        versions = get_agent_versions()
        version_str = f"**Session ID:** `{session_id}`"

        # Initial status
        initial_status = f"""🔍 **Investigation Started**

**Topic:** {topic}
**Depth:** {depth}
**Started:** {start_time.strftime('%H:%M:%S')}
**Session ID:** `{session_id}`

⏳ **Initializing AI agents...**
- Loading {versions['agents']['mcp_researcher']['model']} for research
- Loading {versions['agents']['architect']['model']} for architecture
- Preparing tools and workflows
"""

        yield "*Investigation in progress...*", initial_status, version_str

        # Create crew
        session_logger.log_event("crew_init", "Initializing CrewAI workflow")
        crew_status = initial_status + "\n✅ Agents initialized! Starting investigation...\n"
        yield "*Investigation in progress...*", crew_status, version_str

        crew = MCPInvestigationCrew(verbose=True, session_logger=session_logger)

        # Phase 1: MCP Research
        session_logger.start_phase(1, "MCP Research")
        phase1_status = crew_status + f"""
🔬 **Phase 1/4: MCP Research**
**Agent:** MCP Researcher ({versions['agents']['mcp_researcher']['model']})
**Status:** Searching web for MCP documentation and best practices...
**Tools:** Web search, Serper API
"""
        yield "*Investigation in progress...*", phase1_status, version_str

        # Phase 2: Technical Analysis
        session_logger.start_phase(2, "Technical Analysis")
        phase2_status = phase1_status + f"""
💻 **Phase 2/4: Technical Analysis**
**Agent:** Technical Analyst ({versions['agents']['tech_analyst']['model']})
**Status:** Analyzing GitHub repositories and code examples...
**Tools:** GitHub search, code analysis
"""
        yield "*Investigation in progress...*", phase2_status, version_str

        # Phase 3: Architecture Design
        session_logger.start_phase(3, "Architecture Design")
        phase3_status = phase2_status + f"""
🏗️ **Phase 3/4: Architecture Design**
**Agent:** System Architect ({versions['agents']['architect']['model']})
**Status:** Synthesizing research and designing optimal architecture...
**Tools:** Analysis, design patterns
"""
        yield "*Investigation in progress...*", phase3_status, version_str

        # Phase 4: Documentation
        session_logger.start_phase(4, "Documentation")
        phase4_status = phase3_status + f"""
✍️ **Phase 4/4: Documentation**
**Agent:** Technical Writer ({versions['agents']['technical_writer']['model']})
**Status:** Creating comprehensive markdown report...
**Tools:** Markdown generation, formatting
"""
        yield "*Investigation in progress...*", phase4_status, version_str

        # Run actual investigation
        result = crew.investigate(topic=topic, depth=depth)

        # Get output file path
        output_dir = Path("outputs")
        latest_file = max(output_dir.glob("investigation_*.md"), key=lambda x: x.stat().st_mtime, default=None)

        # Complete session logging
        session_logger.complete_investigation(success=True, output_file=str(latest_file) if latest_file else None)

        # Export session log
        session_log_file = session_logger.export_session_log()

        # Clean result - remove markdown code fence wrapper if present
        result_str = str(result).strip()
        if result_str.startswith('```markdown'):
            # Remove opening fence and closing fence
            result_str = result_str[len('```markdown'):].strip()
            if result_str.endswith('```'):
                result_str = result_str[:-3].strip()
        elif result_str.startswith('```'):
            # Remove generic code fence
            result_str = result_str[3:].strip()
            if result_str.endswith('```'):
                result_str = result_str[:-3].strip()

        # Convert markdown to HTML
        result_html = markdown.markdown(
            result_str,
            extensions=['extra', 'codehilite', 'tables', 'fenced_code']
        )

        # Final success
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        success_msg = f"""✅ **Investigation Complete!**

**Topic:** {topic}
**Completed:** {end_time.strftime('%H:%M:%S')}
**Duration:** {duration:.1f} seconds
**Session ID:** `{session_id}`
**Session Log:** `{session_log_file}`

🎉 Report generated successfully!
📁 Output: `{latest_file}`
"""

        yield result_html, success_msg, version_str

    except Exception as e:
        session_logger.complete_investigation(success=False)
        error_msg = f"""❌ Error during investigation:

**Session ID:** `{session_id}`
**Error:**
```
{str(e)}
```
"""
        yield f"<p style='color: red;'>Investigation failed. See status for details.</p>", error_msg, version_str


def get_example_topics():
    """Return example investigation topics."""
    return [
        "web scraping MCP tool architecture",
        "PostgreSQL database MCP tool",
        "file system MCP tool",
        "REST API integration MCP tool",
        "Slack messaging MCP tool",
        "GitHub integration MCP tool",
        "Google Calendar MCP tool",
        "Email automation MCP tool"
    ]


def list_recent_investigations():
    """List recent investigation reports."""
    output_dir = Path("outputs")
    if not output_dir.exists():
        return "No investigations yet."

    reports = sorted(output_dir.glob("investigation_*.md"), key=lambda x: x.stat().st_mtime, reverse=True)

    if not reports:
        return "No investigations yet."

    result = "## Recent Investigations\n\n"
    for i, report in enumerate(reports[:10], 1):
        timestamp = datetime.fromtimestamp(report.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        topic = report.stem.replace("investigation_", "").replace("_", " ")
        size = report.stat().st_size / 1024  # KB
        result += f"{i}. **{topic}** - {timestamp} ({size:.1f} KB)\n"

    return result


def load_session_logs():
    """List available session logs."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        return "No session logs yet."

    log_files = sorted(logs_dir.glob("session_*_events.json"), key=lambda x: x.stat().st_mtime, reverse=True)

    if not log_files:
        return "No session logs yet."

    result = "## Session Logs\n\n"
    for i, log_file in enumerate(log_files[:10], 1):
        timestamp = datetime.fromtimestamp(log_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        session_id = log_file.stem.split('_')[1]
        result += f"{i}. **Session {session_id}** - {timestamp}\n"

    return result


# Create enhanced Gradio interface
with gr.Blocks(title="MCP Investigation Tool - Enhanced") as demo:
    gr.Markdown("""
    # 🔍 MCP Investigation Tool (Enhanced)

    **Multi-Agent AI Research System** with session tracking, version display, and real-time progress.

    Enter a topic and let our specialized AI agents research, analyze, and design comprehensive architecture documentation.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            topic_input = gr.Textbox(
                label="Investigation Topic",
                placeholder="e.g., web scraping MCP tool architecture",
                lines=2,
                info="What MCP tool architecture would you like to investigate?"
            )

            depth_selector = gr.Radio(
                choices=["quick", "standard", "comprehensive"],
                value="comprehensive",
                label="Investigation Depth",
                info="Comprehensive provides the most detailed analysis"
            )

            with gr.Row():
                investigate_btn = gr.Button("🚀 Start Investigation", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", size="lg")

        with gr.Column(scale=1):
            gr.Markdown("### 💡 Example Topics")
            examples = gr.Examples(
                examples=[[topic] for topic in get_example_topics()],
                inputs=[topic_input],
                label=None
            )

            # Version and session info
            session_info = gr.Markdown(
                value=format_version_info(),
                label="System Info"
            )

    gr.Markdown("---")

    status_output = gr.Markdown(
        label="🔄 Status & Progress",
        value="Ready to investigate. Enter a topic above and click **Start Investigation**.",
        elem_classes=["status-box"]
    )

    gr.Markdown("---")

    report_output = gr.HTML(
        label="📄 Investigation Report",
        value="<p style='color: #666; font-style: italic;'>No investigation yet. Your report will appear here.</p>",
        elem_classes=["markdown-output"]
    )

    gr.Markdown("---")

    with gr.Accordion("📚 Recent Investigations", open=False):
        recent_list = gr.Markdown(value=list_recent_investigations())
        refresh_btn = gr.Button("🔄 Refresh List")

    with gr.Accordion("📋 Session Logs", open=False):
        session_logs = gr.Markdown(value=load_session_logs())
        refresh_logs_btn = gr.Button("🔄 Refresh Logs")

    # Get version info for footer
    footer_versions = get_agent_versions()

    gr.Markdown(f"""
    ---

    ### 🤖 How It Works

    1. **MCP Researcher** 🔬 ({footer_versions['agents']['mcp_researcher']['model']}) - Searches web for MCP documentation and best practices
    2. **Technical Analyst** 💻 ({footer_versions['agents']['tech_analyst']['model']}) - Analyzes GitHub code examples and patterns
    3. **System Architect** 🏗️ ({footer_versions['agents']['architect']['model']}) - Designs optimal architecture with trade-off analysis
    4. **Technical Writer** ✍️ ({footer_versions['agents']['technical_writer']['model']}) - Creates comprehensive markdown documentation

    **Time:** 3-5 minutes per investigation
    **Cost:** ~$0.15-0.20 per investigation

    ---

    {format_version_info()}
    """)

    # Event handlers
    investigate_btn.click(
        fn=investigate_topic,
        inputs=[topic_input, depth_selector],
        outputs=[report_output, status_output, session_info]
    )

    clear_btn.click(
        fn=lambda: ("", "comprehensive", "<p style='color: #666;'>Ready to investigate.</p>", "Ready to investigate.", format_version_info()),
        outputs=[topic_input, depth_selector, report_output, status_output, session_info]
    )

    refresh_btn.click(
        fn=list_recent_investigations,
        outputs=[recent_list]
    )

    refresh_logs_btn.click(
        fn=load_session_logs,
        outputs=[session_logs]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,  # Different port to avoid conflict
        share=False,
        show_error=True,
        theme=gr.themes.Soft(),
        css="""
        .markdown-output {
            max-height: 600px;
            overflow-y: auto;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
        }
        .status-box {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
        }
        """
    )
