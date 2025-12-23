# MCP Investigation Tool

A multi-agent research system for investigating MCP (Model Context Protocol) tool architectures and patterns.

## Features

- 🎨 **Beautiful Web UI** - Gradio-powered interface
- 🔍 Automated research using specialized AI agents
- 📊 Architecture analysis and recommendations
- 📝 Comprehensive markdown reports
- 💰 Cost-efficient (< $0.50 per investigation)
- ⚡ Fast (< 5 minutes per investigation)

## Architecture

The system uses 4 specialized agents working sequentially:

1. **MCP Research Agent** - Gathers MCP documentation and best practices
2. **Technical Research Agent** - Analyzes code examples and patterns
3. **Architecture Analyst** - Synthesizes findings and designs solutions
4. **Technical Writer** - Creates comprehensive documentation

See [MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md) for detailed architecture.

## Quick Start

### Option 1: Web UI (Gradio - Recommended for Quick Start)

```bash
# Launch the Gradio web interface
./run_ui.sh

# Or directly
venv/bin/python app.py
```

Then open: **http://localhost:7860**

See [UI_GUIDE.md](UI_GUIDE.md) for full UI documentation.

### Option 2: REST API + Lovable Frontend

For a production-ready UI with modern React:

```bash
# Launch the REST API
./run_api.sh
```

Then create your Lovable frontend - see [LOVABLE_INTEGRATION.md](LOVABLE_INTEGRATION.md) for details.

API available at:
- **Endpoints:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs

### Option 3: Command Line

### 1. Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required: OPENAI_API_KEY
# Optional: SERPER_API_KEY (for better web search)
```

### 3. Run Investigation

```bash
python src/main.py
```

Or use programmatically:

```python
from src.crew import MCPInvestigationCrew

crew = MCPInvestigationCrew()
result = crew.investigate(
    topic="web scraping MCP tool architecture",
    depth="comprehensive"
)
```

## Project Structure

```
investigation-tool/
├── src/
│   ├── agents/          # Agent definitions
│   ├── tasks/           # Task definitions
│   ├── tools/           # Custom tools
│   ├── crew.py          # Main orchestration
│   └── main.py          # Entry point
├── outputs/             # Generated reports
├── AGENTS.md            # Original design document
├── MVP_ARCHITECTURE.md  # MVP architecture
└── README.md            # This file
```

## Cost Estimation

Per investigation (approximate):
- Research: ~$0.002
- Analysis: ~$0.05
- Documentation: ~$0.06
- **Total: ~$0.11**

## Roadmap

### MVP (Current)
- [x] Architecture design
- [ ] Basic agents
- [ ] Sequential execution
- [ ] Markdown reports

### Future
- [ ] Parallel agent execution
- [ ] Advanced model selection
- [ ] Web UI
- [ ] Database storage
- [ ] MCP protocol integration

## Documentation

- [AGENTS.md](AGENTS.md) - Original multi-agent system design
- [MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md) - MVP architecture details
- [IMPLEMENTATION_STRATEGIES.md](IMPLEMENTATION_STRATEGIES.md) - Strategy comparison

## License

MIT
