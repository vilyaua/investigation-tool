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

### Option 1: Docker (Recommended)

```bash
# Start all services with Docker
docker-compose up -d

# Access:
# - Gradio UI: http://localhost:7860
# - REST API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for complete Docker documentation.

### Option 2: Web UI (Gradio - Local Development)

```bash
# Launch the Gradio web interface
./run_ui.sh

# Or directly
venv/bin/python app.py
```

Then open: **http://localhost:7860**

See [UI_GUIDE.md](UI_GUIDE.md) for full UI documentation.

### Option 3: REST API + Lovable Frontend

For a production-ready UI with modern React:

```bash
# Launch the REST API
./run_api.sh
```

Then create your Lovable frontend - see [LOVABLE_INTEGRATION.md](LOVABLE_INTEGRATION.md) for details.

**Lovable Code Location:** Place your exported Lovable code in the `frontend/` directory.

API available at:
- **Endpoints:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs

### Option 4: Command Line

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

### Getting Started
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick commands cheat sheet
- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Complete setup guide

### Development Guides
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker development & deployment
- **[LOVABLE_INTEGRATION.md](LOVABLE_INTEGRATION.md)** - Lovable.dev frontend setup
- **[UI_GUIDE.md](UI_GUIDE.md)** - Gradio UI documentation
- **[frontend/README.md](frontend/README.md)** - Frontend-specific guide

### Architecture & Design
- [AGENTS.md](AGENTS.md) - Original multi-agent system design
- [MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md) - MVP architecture details
- [IMPLEMENTATION_STRATEGIES.md](IMPLEMENTATION_STRATEGIES.md) - Strategy comparison

## License

MIT
