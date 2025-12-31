#!/usr/bin/env python3
"""
Gradio Web UI for MCP Investigation Tool
"""

import gradio as gr
from datetime import datetime
from pathlib import Path

from src.crew import MCPInvestigationCrew


def investigate_topic(topic: str, depth: str):
    """
    Run an investigation and yield progress updates.

    Args:
        topic: Investigation topic
        depth: Investigation depth

    Yields:
        Tuple of (report_markdown, status_message)
    """
    if not topic or not topic.strip():
        yield "❌ Please enter a topic to investigate.", "Error: No topic provided"
        return

    try:
        # Initial status
        start_time = datetime.now()
        initial_status = f"🔍 **Investigation Started**\n\n**Topic:** {topic}\n**Depth:** {depth}\n**Started:** {start_time.strftime('%H:%M:%S')}\n\n"
        initial_status += "⏳ Initializing agents...\n"

        yield "*Investigation in progress...*", initial_status

        # Phase 1: MCP Research
        phase1_status = initial_status + "\n🔬 **Phase 1/4: MCP Research**\n"
        phase1_status += "Searching for MCP documentation and best practices...\n"
        yield "*Investigation in progress...*", phase1_status

        # Create crew and run investigation
        crew = MCPInvestigationCrew(verbose=True)

        # Phase 2: Technical Analysis (simulated - actual work happens in crew)
        phase2_status = phase1_status + "\n💻 **Phase 2/4: Technical Analysis**\n"
        phase2_status += "Analyzing GitHub code examples and patterns...\n"
        yield "*Investigation in progress...*", phase2_status

        # Phase 3: Architecture Design
        phase3_status = phase2_status + "\n🏗️ **Phase 3/4: Architecture Design**\n"
        phase3_status += "Synthesizing findings and designing architecture...\n"
        yield "*Investigation in progress...*", phase3_status

        # Phase 4: Documentation
        phase4_status = phase3_status + "\n✍️ **Phase 4/4: Documentation**\n"
        phase4_status += "Creating comprehensive markdown report...\n"
        yield "*Investigation in progress...*", phase4_status

        # Run actual investigation
        result = crew.investigate(topic=topic, depth=depth)

        # Final success
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        success_msg = f"✅ **Investigation Complete!**\n\n**Topic:** {topic}\n**Completed:** {end_time.strftime('%H:%M:%S')}\n**Duration:** {duration:.1f} seconds\n\n🎉 Report generated successfully!"

        yield str(result), success_msg

    except Exception as e:
        error_msg = f"❌ Error during investigation:\n\n```\n{str(e)}\n```"
        yield error_msg, "Investigation failed"


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


# Create Gradio interface
with gr.Blocks(title="MCP Investigation Tool") as demo:
    gr.Markdown("""
    # 🔍 MCP Investigation Tool

    **Multi-Agent AI Research System** for investigating MCP (Model Context Protocol) tool architectures.

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

    gr.Markdown("---")

    status_output = gr.Markdown(
        label="Status",
        value="Ready to investigate. Enter a topic above and click **Start Investigation**."
    )

    gr.Markdown("---")

    report_output = gr.Markdown(
        label="Investigation Report",
        value="*No investigation yet. Your report will appear here.*"
    )

    gr.Markdown("---")

    with gr.Accordion("📚 Recent Investigations", open=False):
        recent_list = gr.Markdown(value=list_recent_investigations())
        refresh_btn = gr.Button("🔄 Refresh List")

    gr.Markdown("""
    ---

    ### 🤖 How It Works

    1. **MCP Researcher** 🔬 - Searches web for MCP documentation and best practices
    2. **Technical Analyst** 💻 - Analyzes GitHub code examples and patterns
    3. **System Architect** 🏗️ - Designs optimal architecture with trade-off analysis
    4. **Technical Writer** ✍️ - Creates comprehensive markdown documentation

    **Time:** 3-5 minutes per investigation
    **Cost:** ~$0.15-0.20 per investigation

    ---

    **Built with:** CrewAI • OpenAI GPT-4o • Gradio
    **Version:** MVP 1.0
    """)

    # Event handlers
    investigate_btn.click(
        fn=investigate_topic,
        inputs=[topic_input, depth_selector],
        outputs=[report_output, status_output]
    )

    clear_btn.click(
        fn=lambda: ("", "comprehensive", "Ready to investigate.", "*No investigation yet.*"),
        outputs=[topic_input, depth_selector, status_output, report_output]
    )

    refresh_btn.click(
        fn=list_recent_investigations,
        outputs=[recent_list]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True to create a public link
        show_error=True,
        theme=gr.themes.Soft()
    )
