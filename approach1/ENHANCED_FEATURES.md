# Enhanced Features Guide

Complete guide to the new enhanced features in the MCP Investigation Tool.

## 🎯 What's New

### 1. ✅ Session ID Tracking with Detailed Logging

**Feature:** Every investigation gets a unique session ID for complete traceability.

**Benefits:**
- Track data flow across all agents
- Debug issues with specific investigations
- Audit trail for all operations
- Session-based log files

**Implementation:**
- Located in: `src/utils/logging_config.py`
- Session logs saved to: `logs/session_<id>_<timestamp>.log`
- JSON export: `logs/session_<id>_events.json`

**Usage:**
```python
from src.utils.logging_config import SessionLogger

logger = SessionLogger()
logger.start_investigation("my topic", "comprehensive")
logger.log_agent_action("MCP Researcher", "web search", {"query": "..."})
logger.complete_investigation(success=True)
```

**Log Format:**
```
[2025-12-23 11:20:00] [SESSION:a1b2c3d4] [INFO] INVESTIGATION_START: Starting investigation: configurable mcp tool | Metadata: {"topic": "configurable mcp tool", "depth": "comprehensive"}
[2025-12-23 11:20:05] [SESSION:a1b2c3d4] [INFO] PHASE_START: Phase 1/4: MCP Research | Metadata: {"phase": 1, "phase_name": "MCP Research"}
```

### 2. ✅ Agent Version Display

**Feature:** UI shows which agent versions were used for each investigation.

**Benefits:**
- Know exactly what versions produced a report
- Track changes across agent updates
- Debug version-specific issues
- Audit compliance

**Implementation:**
- Located in: `src/utils/version_info.py`
- Shows:
  - App version
  - Git commit (if available)
  - Each agent version
  - Dependency versions (CrewAI, OpenAI, Gradio)

**Displayed in UI:**
```
### 🔧 System Information

**App Version:** 1.0.0
**Git Commit:** abc1234

**Agent Versions:**
- MCP Researcher: v1.0.0
- Technical Analyst: v1.0.0
- System Architect: v1.0.0
- Technical Writer: v1.0.0

**Dependencies:**
- CrewAI: 1.7.2
- OpenAI: 1.83.0
- Gradio: 6.2.0
```

### 3. ✅ Real-Time Progress Information

**Feature:** Live updates showing exactly what's happening during investigation.

**Benefits:**
- No more wondering if it's stuck
- See which agent is working
- Understand investigation progress
- Transparency into the process

**Updates Include:**
- Session ID assignment
- Phase transitions (1/4, 2/4, etc.)
- Current agent name and version
- Specific task being performed
- Duration tracking

**Example Progress Display:**
```
🔍 Investigation Started

Topic: configurable mcp tool
Depth: comprehensive
Started: 11:15:14
Session ID: a1b2c3d4

⏳ Initializing agents...

🔬 Phase 1/4: MCP Research
Agent: MCP Researcher v1.0.0
Status: Searching for MCP documentation and best practices...

💻 Phase 2/4: Technical Analysis
Agent: Technical Analyst v1.0.0
Status: Analyzing GitHub code examples and patterns...

🏗️ Phase 3/4: Architecture Design
Agent: System Architect v1.0.0
Status: Synthesizing findings and designing architecture...

✍️ Phase 4/4: Documentation
Agent: Technical Writer v1.0.0
Status: Creating comprehensive markdown report...

✅ Investigation Complete!
Completed: 11:20:45
Duration: 331.2 seconds
Session ID: a1b2c3d4
```

### 4. ✅ Proper Markdown Rendering

**Feature:** Reports render as beautifully formatted HTML instead of raw markdown.

**Benefits:**
- Professional-looking reports
- Proper formatting of headers, lists, code blocks
- Syntax highlighting for code
- Tables render correctly
- Links are clickable

**Implementation:**
- Uses Python `markdown` library
- Extensions enabled:
  - `extra` - Extra features
  - `codehilite` - Syntax highlighting
  - `tables` - Table support
  - `fenced_code` - Code blocks

**Before:**
```
# MCP Tool Architecture

## Executive Summary
- **Problem**: Integration complexity
```

**After:**
Renders as properly formatted HTML with:
- Large, bold headers
- Nested bullet points
- Syntax-highlighted code blocks
- Clickable links
- Formatted tables

## 📁 File Structure

```
investigation-tool/
├── src/
│   └── utils/
│       ├── __init__.py
│       ├── logging_config.py       # Session logging
│       └── version_info.py         # Version tracking
├── logs/                            # Session logs directory
│   ├── session_<id>_<timestamp>.log
│   └── session_<id>_events.json
├── app.py                           # Original UI
├── app_enhanced.py                  # Enhanced UI ⭐
├── run_ui.sh                        # Original launcher
└── run_enhanced_ui.sh              # Enhanced launcher ⭐
```

## 🚀 How to Use

### Launch Enhanced UI

```bash
# Option 1: Using launcher script
./run_enhanced_ui.sh

# Option 2: Direct
venv/bin/python app_enhanced.py
```

**Access:** http://localhost:7861

### Differences from Original

| Feature | Original UI (port 7860) | Enhanced UI (port 7861) |
|---------|------------------------|------------------------|
| Session ID | ❌ No | ✅ Yes |
| Detailed Logs | ❌ No | ✅ Yes (JSON + text) |
| Agent Versions | ❌ No | ✅ Yes |
| Real-time Progress | ⚠️ Basic | ✅ Detailed |
| Markdown Rendering | ⚠️ Basic | ✅ HTML with syntax highlighting |
| Session Log Viewer | ❌ No | ✅ Yes |

### View Session Logs

1. Click "📋 Session Logs" accordion in UI
2. See list of all session logs
3. Or manually check `logs/` directory

**Session Log JSON Format:**
```json
{
  "session_summary": {
    "session_id": "a1b2c3d4",
    "start_time": "2025-12-23T11:15:14",
    "duration_seconds": 331.2,
    "events_count": 15,
    "log_file": "logs/session_a1b2c3d4_20251223_111514.log"
  },
  "events": [
    {
      "timestamp": "2025-12-23T11:15:14",
      "session_id": "a1b2c3d4",
      "event_type": "investigation_start",
      "message": "Starting investigation: configurable mcp tool",
      "topic": "configurable mcp tool",
      "depth": "comprehensive"
    },
    ...
  ]
}
```

## 🔍 Debugging with Session Logs

### Find a Specific Investigation

```bash
# List recent sessions
ls -lt logs/session_*_events.json | head -5

# Search for specific topic
grep -l "specific topic" logs/session_*.log

# View session details
cat logs/session_a1b2c3d4_events.json | jq '.session_summary'
```

### Trace Data Flow

```bash
# Follow a session in real-time (if running)
tail -f logs/session_a1b2c3d4_20251223_111514.log

# See all agent actions
cat logs/session_a1b2c3d4_20251223_111514.log | grep "AGENT_ACTION"

# See all tool uses
cat logs/session_a1b2c3d4_20251223_111514.log | grep "TOOL_USE"
```

### Analyze Investigation Performance

```bash
# Extract timing information
cat logs/session_a1b2c3d4_events.json | jq '.events[] | select(.event_type == "phase_start") | {phase, timestamp}'

# Calculate phase durations
# (Use jq to parse timestamps and calculate differences)
```

## 🐳 Docker Integration

The enhanced features work seamlessly with Docker:

```bash
# Build with enhanced features
docker-compose build

# Run enhanced UI in Docker
docker-compose up -d

# Access logs from container
docker exec mcp-investigation-gradio ls -l logs/

# Copy logs out of container
docker cp mcp-investigation-gradio:/app/logs ./local-logs/
```

## 📊 Monitoring Best Practices

1. **Keep logs for audit trail**
   - Session logs are small (typically < 100KB)
   - Keep for compliance/debugging

2. **Regular cleanup**
   ```bash
   # Remove logs older than 30 days
   find logs/ -name "session_*.log" -mtime +30 -delete
   ```

3. **Monitor log growth**
   ```bash
   du -sh logs/
   ```

4. **Export important sessions**
   - JSON format is portable
   - Easy to analyze with tools like `jq`

## 🎯 Tips & Tricks

### Quick Session Summary

```python
from src.utils.logging_config import SessionLogger

logger = SessionLogger("a1b2c3d4")
summary = logger.get_session_summary()
print(f"Session ran for {summary['duration_seconds']}s")
```

### Add Custom Events

```python
logger.log_event(
    "custom_event",
    "Something interesting happened",
    custom_field="value",
    metadata={"key": "value"}
)
```

### Version Checking in Code

```python
from src.utils.version_info import get_agent_versions

versions = get_agent_versions()
if versions['dependencies']['crewai'] != "1.7.2":
    print("Warning: Unexpected CrewAI version")
```

## 🔄 Migration Guide

### From Original to Enhanced UI

**No breaking changes!** Both UIs can run simultaneously:
- Original: Port 7860
- Enhanced: Port 7861

**To switch:**
1. Stop original: `Ctrl+C` or kill process on port 7860
2. Start enhanced: `./run_enhanced_ui.sh`

**To update Docker:**
- Enhanced UI will be default in future releases
- For now, both are available

## 📝 Future Enhancements

Planned features:
- [ ] Export session logs as CSV
- [ ] Session replay/visualization
- [ ] Performance metrics dashboard
- [ ] Alert on long-running sessions
- [ ] Integration with external monitoring tools

---

**Questions or issues?** Check the session logs first - they contain detailed debugging information!

🎉 Enjoy the enhanced features!
