# Gradio Web UI Guide

## 🚀 Quick Start

Launch the web UI:

```bash
./run_ui.sh
```

Or directly:

```bash
venv/bin/python app.py
```

Then open your browser to: **http://localhost:7860**

---

## 🎨 Features

### Main Interface

- **Investigation Topic Input** - Enter any MCP tool topic to investigate
- **Depth Selector** - Choose quick, standard, or comprehensive analysis
- **Example Topics** - Click to load pre-configured topics
- **Live Status** - See progress as agents work
- **Report Display** - View formatted markdown reports
- **Recent Investigations** - Browse your investigation history

### Example Topics

The UI includes 8 pre-configured example topics:
- Web scraping MCP tool
- PostgreSQL database MCP tool
- File system MCP tool
- REST API integration MCP tool
- Slack messaging MCP tool
- GitHub integration MCP tool
- Google Calendar MCP tool
- Email automation MCP tool

---

## 💡 How to Use

### Run an Investigation

1. **Enter a topic** in the text box
   - Example: "web scraping MCP tool architecture"

2. **Select depth** (recommended: comprehensive)
   - Quick: ~2 min, basic overview
   - Standard: ~3-4 min, good detail
   - Comprehensive: ~4-5 min, full analysis

3. **Click "Start Investigation"**
   - Watch the status panel for progress
   - All 4 agents will work sequentially

4. **View the report**
   - Appears in the markdown panel below
   - Automatically saved to `outputs/` directory

### Browse History

1. Click **"Recent Investigations"** accordion
2. See list of past reports with timestamps
3. Click **"Refresh List"** to update

---

## 🔧 Configuration

### Change Port

Edit `app.py` line near the end:

```python
demo.launch(
    server_port=7860,  # Change this
    ...
)
```

### Enable Public Sharing

Set `share=True` in `app.py`:

```python
demo.launch(
    share=True,  # Creates public URL
    ...
)
```

This creates a temporary public URL (valid for 72 hours) that you can share.

### Enable Password Protection

Add authentication:

```python
demo.launch(
    auth=("username", "password"),
    ...
)
```

---

## 🌐 Access Options

### Local Only
```
http://localhost:7860
```

### Network Access
```
http://YOUR_IP:7860
```
Others on your network can access it.

### Public URL (with share=True)
```
https://xxxxx.gradio.live
```
Temporary public URL for sharing.

---

## 📊 UI Components

### Top Section
- Topic input field
- Depth selector
- Action buttons (Start, Clear)
- Example topics

### Middle Section
- Status panel (shows agent progress)
- Report output (formatted markdown)

### Bottom Section
- Recent investigations list
- How it works info
- System details

---

## 🎯 Tips

1. **Start with examples** - Click an example topic to see how it works

2. **Use comprehensive depth** - Best results for architecture design

3. **Be specific** - "PostgreSQL MCP tool with connection pooling" is better than "database tool"

4. **Check recent investigations** - Avoid re-running the same topic

5. **Save good reports** - Copy markdown to your docs if needed

---

## 🐛 Troubleshooting

### Port Already in Use

Change the port in `app.py` or kill the existing process:

```bash
lsof -ti:7860 | xargs kill -9
```

### UI Won't Load

Check that the server started:

```bash
tail -f logs/gradio.log
```

### Investigation Fails

1. Check `.env` has valid `OPENAI_API_KEY`
2. Ensure you have API credits
3. Check internet connection for web search
4. Look at terminal for error messages

---

## 🚀 Deployment

### Local Development
```bash
./run_ui.sh
```

### Production (Hugging Face Spaces)

1. Create account at https://huggingface.co/spaces
2. Create new Space (Gradio SDK)
3. Push your code:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/mcp-investigation
   git push hf main
   ```

### Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

```bash
docker build -t mcp-investigation-ui .
docker run -p 7860:7860 mcp-investigation-ui
```

---

## 📈 Monitoring

The UI automatically:
- Saves all reports to `outputs/`
- Shows live agent status
- Tracks investigation history
- Displays errors clearly

---

## 🎨 Customization

### Change Theme

Edit `app.py`:

```python
with gr.Blocks(theme=gr.themes.Soft()) as demo:
```

Available themes:
- `gr.themes.Soft()` (current)
- `gr.themes.Default()`
- `gr.themes.Glass()`
- `gr.themes.Monochrome()`

### Add Custom Examples

Edit the `get_example_topics()` function in `app.py`.

### Modify Layout

The UI uses Gradio Blocks - rearrange components as needed.

---

## 🔗 Resources

- **Gradio Docs**: https://gradio.app/docs
- **Gradio Themes**: https://gradio.app/theming-guide
- **Hugging Face Spaces**: https://huggingface.co/spaces

---

Enjoy your MCP Investigation Tool UI! 🎉
