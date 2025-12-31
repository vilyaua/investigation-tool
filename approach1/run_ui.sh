#!/bin/bash
# Launch the Gradio UI for MCP Investigation Tool

echo "🚀 Starting MCP Investigation Tool UI..."
echo ""
echo "The UI will be available at:"
echo "  Local: http://localhost:7860"
echo "  Network: http://0.0.0.0:7860"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

venv/bin/python app.py
