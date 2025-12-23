# Lovable.dev Integration Guide

This guide shows how to integrate the MCP Investigation Tool with a Lovable.dev frontend.

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Lovable.dev    │  HTTP   │   FastAPI        │ Python  │   CrewAI        │
│  React Frontend │ ──────> │   REST API       │ ──────> │   Multi-Agent   │
│  (Port 3000)    │ <────── │   (Port 8000)    │ <────── │   System        │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

## Quick Start

### 1. Start the REST API

```bash
./run_api.sh
```

The API will be available at:
- **API:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 2. Create Your Lovable Project

Go to [lovable.dev](https://lovable.dev) and create a new project with this prompt:

```
Create a modern web UI for an AI-powered MCP investigation tool.

The app should have:

1. Main investigation form with:
   - Text input for investigation topic
   - Dropdown for depth (quick/standard/comprehensive)
   - Submit button
   - Example topics as chips/buttons

2. Results display with:
   - Live status updates showing current phase
   - Markdown viewer for the final report
   - Duration and timestamp info

3. History sidebar showing:
   - List of recent investigations
   - Ability to click and view past reports

4. Modern design with:
   - Dark mode support
   - Responsive layout
   - Loading states and animations
   - Error handling

The UI should call these API endpoints:
- POST /api/investigate - Start investigation
- GET /api/status/{topic} - Check status
- GET /api/recent - List recent investigations
- GET /api/report/{filename} - Get report content

Use modern React with TypeScript, TailwindCSS, and shadcn/ui components.
```

### 3. Configure API Connection

In your Lovable project, update the API base URL:

```typescript
// src/lib/api.ts
const API_BASE_URL = 'http://localhost:8000';

export async function startInvestigation(topic: string, depth: string) {
  const response = await fetch(`${API_BASE_URL}/api/investigate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ topic, depth }),
  });

  if (!response.ok) {
    throw new Error('Investigation failed');
  }

  return response.json();
}

export async function getStatus(topic: string) {
  const response = await fetch(`${API_BASE_URL}/api/status/${topic}`);
  return response.json();
}

export async function getRecentInvestigations() {
  const response = await fetch(`${API_BASE_URL}/api/recent`);
  return response.json();
}

export async function getReport(filename: string) {
  const response = await fetch(`${API_BASE_URL}/api/report/${filename}`);
  return response.json();
}
```

## API Endpoints

### POST /api/investigate

Start a new investigation.

**Request:**
```json
{
  "topic": "web scraping MCP tool architecture",
  "depth": "comprehensive"
}
```

**Response:**
```json
{
  "report": "# Web Scraping MCP Tool Architecture\n\n...",
  "topic": "web scraping MCP tool architecture",
  "depth": "comprehensive",
  "started_at": "2024-01-15T10:30:00",
  "completed_at": "2024-01-15T10:34:30",
  "duration_seconds": 270.5,
  "status": "completed"
}
```

### GET /api/status/{topic}

Get investigation status (useful for polling during long-running investigations).

**Response:**
```json
{
  "topic": "web scraping MCP tool architecture",
  "status": "running",
  "phase": "phase_2",
  "message": "Analyzing GitHub code examples..."
}
```

### GET /api/recent

List recent investigations.

**Response:**
```json
{
  "investigations": [
    {
      "topic": "web scraping MCP tool",
      "filename": "investigation_web_scraping_MCP_tool_20240115_103000.md",
      "timestamp": "2024-01-15T10:30:00",
      "size_kb": 45.3
    }
  ]
}
```

### GET /api/report/{filename}

Get a specific report.

**Response:**
```json
{
  "filename": "investigation_web_scraping_MCP_tool_20240115_103000.md",
  "content": "# Web Scraping MCP Tool Architecture\n\n..."
}
```

## Example React Component

```typescript
import { useState } from 'react';
import { startInvestigation } from '@/lib/api';

export function InvestigationForm() {
  const [topic, setTopic] = useState('');
  const [depth, setDepth] = useState('comprehensive');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = await startInvestigation(topic, depth);
      setResult(data);
    } catch (error) {
      console.error('Investigation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter investigation topic..."
      />

      <select value={depth} onChange={(e) => setDepth(e.target.value)}>
        <option value="quick">Quick</option>
        <option value="standard">Standard</option>
        <option value="comprehensive">Comprehensive</option>
      </select>

      <button type="submit" disabled={loading}>
        {loading ? 'Investigating...' : 'Start Investigation'}
      </button>

      {result && (
        <div>
          <h2>Report</h2>
          <p>Duration: {result.duration_seconds}s</p>
          <div dangerouslySetInnerHTML={{ __html: result.report }} />
        </div>
      )}
    </form>
  );
}
```

## Development

### Run API Only
```bash
./run_api.sh
```

### Run Gradio UI Only
```bash
./run_ui.sh
```

### Run Both
```bash
# Terminal 1
./run_api.sh

# Terminal 2
./run_ui.sh
```

## Production Deployment

### Backend (FastAPI)

Deploy to:
- **Railway.app**
- **Render.com**
- **Fly.io**
- **AWS Lambda** (with Mangum adapter)

Example Railway deployment:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Frontend (Lovable)

Lovable automatically deploys your frontend. Update the API base URL to your production backend:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://your-api.railway.app';
```

## CORS Configuration

For production, update CORS settings in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-lovable-app.lovable.app",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Environment Variables

### Backend (.env)
```bash
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...  # Optional
```

### Frontend (Lovable Environment Variables)
```bash
NEXT_PUBLIC_API_URL=https://your-api.railway.app
```

## Testing

Test the API with curl:

```bash
# Start investigation
curl -X POST http://localhost:8000/api/investigate \
  -H "Content-Type: application/json" \
  -d '{"topic": "file system MCP tool", "depth": "quick"}'

# Check status
curl http://localhost:8000/api/status/file%20system%20MCP%20tool

# List recent
curl http://localhost:8000/api/recent
```

Or use the interactive docs at http://localhost:8000/docs

## Next Steps

1. Start the API: `./run_api.sh`
2. Open http://localhost:8000/docs to test endpoints
3. Create your Lovable frontend with the prompt above
4. Connect your frontend to the API
5. Deploy both services to production

## Support

- **API Issues:** Check logs and `/docs` endpoint
- **Lovable Issues:** Use Lovable's built-in support
- **General Questions:** See README.md

---

Enjoy building with Lovable! 🎉
