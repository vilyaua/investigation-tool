#!/bin/bash
# Launch the FastAPI REST API for MCP Investigation Tool

echo "🚀 Starting MCP Investigation REST API..."
echo ""
echo "The API will be available at:"
echo "  Local: http://localhost:8000"
echo "  Network: http://0.0.0.0:8000"
echo "  Docs: http://localhost:8000/docs"
echo "  ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

venv/bin/python api.py
