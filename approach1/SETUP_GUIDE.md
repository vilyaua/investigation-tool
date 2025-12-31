# Setup Guide - MCP Investigation Tool MVP

## Quick Start (5 minutes)

### 1. Prerequisites

- Python 3.11 or higher
- OpenAI API key
- (Optional) Serper API key for better web search

### 2. Installation Steps

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env

# 5. Edit .env file and add your API keys
# Required: OPENAI_API_KEY=sk-...
# Optional: SERPER_API_KEY=...
```

### 3. Run Your First Investigation

```bash
# Option 1: Interactive CLI
python src/main.py

# Option 2: Programmatic usage
python -c "
from src.crew import MCPInvestigationCrew
crew = MCPInvestigationCrew()
crew.investigate('web scraping MCP tool')
"
```

### 4. Check Output

```bash
# Reports are saved in the outputs/ directory
ls -lh outputs/
```

---

## Configuration

### Environment Variables (.env)

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (for better web search)
SERPER_API_KEY=your-serper-key-here

# Model Configuration (optional, defaults shown)
DEFAULT_RESEARCH_MODEL=gpt-4o-mini
DEFAULT_ANALYSIS_MODEL=gpt-4o

# Output Settings (optional)
OUTPUT_DIR=outputs
```

### API Keys

**OpenAI API Key** (Required)
1. Go to https://platform.openai.com/api-keys
2. Create a new secret key
3. Add to .env file

**Serper API Key** (Optional, but recommended)
1. Go to https://serper.dev
2. Sign up (free tier available)
3. Copy your API key
4. Add to .env file

If Serper key is not provided, the tool will use DuckDuckGo search (free, but less comprehensive).

---

## Project Structure

```
investigation-tool/
├── .env                    # Your API keys (create from .env.example)
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md              # Project overview
├── SETUP_GUIDE.md         # This file
├── MVP_ARCHITECTURE.md    # Architecture documentation
├── AGENTS.md              # Original design document
├── IMPLEMENTATION_STRATEGIES.md  # Strategy comparison
│
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── crew.py            # Main orchestration
│   ├── main.py            # CLI entry point
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── mcp_researcher.py    # MCP Research Agent
│   │   ├── tech_analyst.py      # Technical Analyst
│   │   ├── architect.py         # System Architect
│   │   └── writer.py            # Technical Writer
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── investigation_tasks.py  # Task definitions
│   │
│   └── tools/
│       ├── __init__.py
│       ├── web_search.py        # Web search tool
│       └── github_search.py     # GitHub search tool
│
├── outputs/              # Generated investigation reports
└── tests/                # Tests
    └── test_basic.py
```

---

## Usage Examples

### Example 1: Web Scraping MCP Tool

```python
from src.crew import MCPInvestigationCrew

crew = MCPInvestigationCrew()
result = crew.investigate(
    topic="web scraping MCP tool architecture",
    depth="comprehensive"
)
print(result)
```

### Example 2: Database MCP Tool

```python
from src.crew import MCPInvestigationCrew

crew = MCPInvestigationCrew()
result = crew.investigate(
    topic="PostgreSQL database MCP tool",
    depth="standard"
)
```

### Example 3: File System MCP Tool

```bash
# Using CLI
python src/main.py
# When prompted, enter: "file system MCP tool architecture"
```

---

## Troubleshooting

### Import Errors

If you see import errors:

```bash
# Make sure you're in the project root directory
cd /path/to/investigation-tool

# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Errors

```
Error: openai_api_key field required
```

**Solution**: Create `.env` file from `.env.example` and add your OpenAI API key.

### Module Not Found Errors

If you see "ModuleNotFoundError":

```bash
# Run from project root
cd /path/to/investigation-tool

# Use python -m to run as module
python -m src.main
```

### Web Search Not Working

If web search fails:

1. **With Serper**: Check your Serper API key in `.env`
2. **Without Serper**: DuckDuckGo may have rate limits, wait a few seconds and retry

---

## Running Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run tests
pytest tests/ -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

---

## Development Tips

### Enable Debug Mode

Edit `src/config.py`:

```python
verbose: bool = True  # Already default
```

Or set in .env:

```bash
VERBOSE=true
```

### Adjust Model Selection

For cost savings during development:

```bash
# In .env
DEFAULT_RESEARCH_MODEL=gpt-4o-mini
DEFAULT_ANALYSIS_MODEL=gpt-4o-mini  # Use mini for all
```

For maximum quality:

```bash
# In .env
DEFAULT_RESEARCH_MODEL=gpt-4o
DEFAULT_ANALYSIS_MODEL=gpt-4o  # Use 4o for all
```

### Customize Agents

Edit agent files in `src/agents/` to customize:
- Role descriptions
- Goals
- Backstories
- Tools available

### Customize Tasks

Edit `src/tasks/investigation_tasks.py` to:
- Modify task descriptions
- Change expected outputs
- Adjust context passing

---

## Cost Estimation

### Per Investigation (Approximate)

With recommended settings:
- Research phase: ~$0.002 (GPT-4o-mini)
- Analysis phase: ~$0.05 (GPT-4o)
- Architecture phase: ~$0.05 (GPT-4o)
- Documentation phase: ~$0.06 (GPT-4o)

**Total: ~$0.11 - $0.20 per investigation**

Running 10 investigations: ~$1-2
Running 100 investigations: ~$10-20

To reduce costs:
- Use GPT-4o-mini for all agents: ~$0.01 per investigation
- Reduce max_iter in agent configs
- Use shorter task descriptions

---

## Next Steps

After your first successful investigation:

1. **Review Output**: Check the generated report in `outputs/`
2. **Iterate**: Try different investigation topics
3. **Customize**: Modify agents and tasks for your specific needs
4. **Extend**: Add new agents or tools as needed

---

## Getting Help

- **Documentation**: See [MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md)
- **Examples**: Check `outputs/` for sample reports
- **Issues**: Review error messages carefully
- **Community**: CrewAI docs at https://docs.crewai.com

---

## Future Enhancements

After MVP is working:

- [ ] Add parallel agent execution
- [ ] Implement advanced model selection logic
- [ ] Create web UI with Gradio/Streamlit
- [ ] Add database storage for reports
- [ ] Integrate native MCP protocol
- [ ] Add more specialized agents
- [ ] Implement conflict resolution
- [ ] Add interactive report generation

See [IMPLEMENTATION_STRATEGIES.md](IMPLEMENTATION_STRATEGIES.md) for long-term roadmap.
