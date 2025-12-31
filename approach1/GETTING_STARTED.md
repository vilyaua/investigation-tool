# Getting Started - MCP Investigation Tool

## 🚀 Quick Start (2 minutes)

```bash
# 1. Create and activate virtual environment
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run your first investigation
python src/main.py
```

## 📋 What You Built

A **multi-agent AI research system** that investigates MCP (Model Context Protocol) tool architectures using 4 specialized agents:

1. **MCP Research Agent** - Gathers documentation and best practices
2. **Technical Analyst** - Analyzes code examples from GitHub
3. **System Architect** - Designs optimal architectures
4. **Technical Writer** - Creates comprehensive reports

## 🎯 What It Does

Input: "I want to investigate [topic] MCP tool architecture"

Output: A comprehensive markdown report with:
- MCP protocol overview
- Existing tools and patterns
- Technical analysis of code examples
- Proposed architecture design
- Implementation guide with code examples
- Deployment recommendations

**Time**: 3-5 minutes per investigation
**Cost**: ~$0.11 - $0.20 per investigation

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | Run this to start an investigation |
| `src/crew.py` | Main orchestration logic |
| `src/agents/*` | Agent definitions (4 specialized agents) |
| `src/tasks/*` | Task definitions (what each agent does) |
| `outputs/` | Generated investigation reports |
| `SETUP_GUIDE.md` | Detailed setup instructions |
| `MVP_ARCHITECTURE.md` | Architecture documentation |

## 🔧 Configuration

Edit `.env` to configure:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (improves web search)
SERPER_API_KEY=your-serper-key

# Model selection (default: gpt-4o-mini for research, gpt-4o for analysis)
DEFAULT_RESEARCH_MODEL=gpt-4o-mini
DEFAULT_ANALYSIS_MODEL=gpt-4o
```

## 💡 Example Topics to Investigate

Try investigating these MCP tool architectures:

- "web scraping MCP tool"
- "PostgreSQL database MCP tool"
- "file system MCP tool"
- "REST API MCP tool"
- "Slack integration MCP tool"
- "GitHub integration MCP tool"

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup & troubleshooting
- **[MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md)** - Architecture design
- **[IMPLEMENTATION_STRATEGIES.md](IMPLEMENTATION_STRATEGIES.md)** - Why CrewAI was chosen
- **[AGENTS.md](AGENTS.md)** - Original design document

## 🎓 Understanding the Code

### How It Works

1. **User provides topic** → "web scraping MCP tool"

2. **Phase 1: Research** (MCP Research Agent)
   - Searches web for MCP documentation
   - Gathers best practices
   - Finds existing tools

3. **Phase 2: Analysis** (Technical Analyst)
   - Searches GitHub for code examples
   - Analyzes implementation patterns
   - Extracts technical insights

4. **Phase 3: Design** (System Architect)
   - Synthesizes findings
   - Designs optimal architecture
   - Analyzes trade-offs

5. **Phase 4: Documentation** (Technical Writer)
   - Creates comprehensive report
   - Includes code examples
   - Provides implementation guide

6. **Output saved** → `outputs/investigation_*.md`

### Customization

Want to modify the tool?

- **Change agent behavior**: Edit files in `src/agents/`
- **Modify tasks**: Edit `src/tasks/investigation_tasks.py`
- **Add tools**: Create new tools in `src/tools/`
- **Adjust models**: Change model names in `.env`

## 🚦 Next Steps

### After Your First Investigation:

1. **Review the output**
   ```bash
   ls -lh outputs/
   cat outputs/investigation_*.md
   ```

2. **Try different topics** - Experiment with various MCP tool types

3. **Customize agents** - Modify agent backstories and goals

4. **Add features** - See [Future Enhancements](#future-enhancements)

### Future Enhancements

Once you're comfortable with the MVP:

- [ ] Add parallel agent execution
- [ ] Create web UI (Gradio/Streamlit)
- [ ] Integrate native MCP protocol
- [ ] Add database storage
- [ ] Implement caching
- [ ] Add more specialized agents

## 🆘 Troubleshooting

**"Module not found" errors**
```bash
# Ensure you're in project root and venv is activated
cd investigation-tool
source venv/bin/activate
pip install -r requirements.txt
```

**"API key not found" errors**
```bash
# Check .env file exists and has OPENAI_API_KEY
cat .env
```

**Import errors**
```bash
# Run as module from project root
python -m src.main
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.

## 💰 Cost Control

To minimize costs while testing:

```bash
# Use GPT-4o-mini for everything
DEFAULT_RESEARCH_MODEL=gpt-4o-mini
DEFAULT_ANALYSIS_MODEL=gpt-4o-mini  # ~$0.01 per investigation
```

For production quality:

```bash
# Use GPT-4o for analysis (recommended)
DEFAULT_RESEARCH_MODEL=gpt-4o-mini
DEFAULT_ANALYSIS_MODEL=gpt-4o  # ~$0.11 per investigation
```

## 📊 Project Status

✅ **MVP Complete** - All core features implemented:
- 4 specialized agents
- Sequential workflow
- Web & GitHub search
- Markdown report generation
- CLI interface
- Configuration system

🚧 **Future Work** (see IMPLEMENTATION_STRATEGIES.md):
- Parallel execution
- Advanced model selection
- Web UI
- MCP protocol integration

## 🎉 Success Criteria

Your MVP is successful if it can:
- ✅ Accept a research topic
- ✅ Gather MCP information via web search
- ✅ Analyze code examples from GitHub
- ✅ Design an architecture
- ✅ Generate actionable report
- ✅ Complete in < 5 minutes
- ✅ Cost < $0.50 per investigation

---

**Ready to start?**

```bash
python src/main.py
```

Happy investigating! 🔍
