#!/usr/bin/env python3
"""Quick test run of the investigation tool."""

from src.crew import MCPInvestigationCrew

print("=" * 60)
print("MCP Investigation Tool - Test Run")
print("=" * 60)

# Create crew
crew = MCPInvestigationCrew(verbose=True)

# Run a simple investigation
topic = "file system MCP tool"
print(f"\nInvestigating: {topic}\n")

try:
    result = crew.investigate(topic=topic, depth="comprehensive")
    print("\n" + "=" * 60)
    print("Investigation Complete!")
    print("=" * 60)
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
