#!/bin/bash
# Launch the Enhanced Gradio UI for MCP Investigation Tool

echo "🚀 Starting MCP Investigation Tool Enhanced UI..."
echo ""
echo "New features:"
echo "  ✅ Session ID tracking with detailed logs"
echo "  ✅ Agent version display"
echo "  ✅ Real-time progress updates"
echo "  ✅ Proper markdown rendering (HTML)"
echo "  ✅ Session log viewer"
echo ""
echo "The Enhanced UI will be available at:"
echo "  Local: http://localhost:7861"
echo "  Network: http://0.0.0.0:7861"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

venv/bin/python app_enhanced.py
