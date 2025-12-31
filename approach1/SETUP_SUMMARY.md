# Setup Summary - Docker + Lovable Integration

## ✅ What's Been Set Up

### Directory Structure

```
investigation-tool/
├── docker-compose.yml          # Orchestrates all services
├── Dockerfile.api              # FastAPI backend container
├── Dockerfile.gradio           # Gradio UI container
├── .dockerignore               # Optimizes Docker builds
│
├── frontend/                   # 👈 PUT YOUR LOVABLE CODE HERE
│   ├── Dockerfile             # Frontend container config
│   ├── README.md              # Frontend setup guide
│   └── .gitkeep               # Placeholder (delete after adding code)
│
├── src/                       # Python backend code
│   ├── agents/
│   ├── tasks/
│   ├── tools/
│   ├── config.py
│   └── crew.py
│
├── app.py                     # Gradio UI
├── api.py                     # FastAPI REST API
├── run_ui.sh                  # Launch Gradio
├── run_api.sh                 # Launch API
│
├── outputs/                   # Shared reports directory
├── .env                       # Your API keys
│
└── Documentation:
    ├── README.md              # Main readme
    ├── DOCKER_GUIDE.md        # Complete Docker guide
    ├── LOVABLE_INTEGRATION.md # Lovable setup guide
    └── SETUP_SUMMARY.md       # This file
```

## 🎯 Where to Put Your Lovable Code

```bash
frontend/
├── src/              # ← Your Lovable src/ goes here
├── public/           # ← Your Lovable public/ goes here
├── package.json      # ← Your Lovable package.json goes here
├── vite.config.ts    # ← Your Lovable config goes here
└── ... (all other Lovable files)
```

## 🚀 Quick Start Commands

### Start Everything with Docker

```bash
# Make sure you have .env file with API keys
cp .env.example .env
# Edit .env with your keys

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### Access Your Services

| Service | URL | Description |
|---------|-----|-------------|
| Gradio UI | http://localhost:7860 | Simple web interface |
| REST API | http://localhost:8000 | Backend for Lovable |
| API Docs | http://localhost:8000/docs | Interactive API testing |
| Frontend | http://localhost:5173 | Your Lovable UI (after setup) |

## 📝 Workflow: Adding Your Lovable Frontend

### Step 1: Export from Lovable

1. Go to your Lovable project
2. Export/download the project
3. You'll get a ZIP file

### Step 2: Extract to Frontend Directory

```bash
# Option A: Unzip directly
cd investigation-tool/frontend
unzip ~/Downloads/lovable-export.zip -d .

# Option B: Copy files manually
cp -r ~/Downloads/lovable-export/* frontend/
```

### Step 3: Configure API URL

Edit `frontend/src/lib/api.ts` (or wherever you define API calls):

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

Or create `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

### Step 4: Enable in Docker Compose

Edit `docker-compose.yml`, uncomment these lines:

```yaml
# Remove the comments (#) from:
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  # ... etc
```

### Step 5: Run It!

```bash
# From investigation-tool root
docker-compose up -d --build

# Check it's running
docker-compose ps

# View logs
docker-compose logs -f frontend
```

Visit http://localhost:5173 🎉

## 🛠️ Development Workflow

### Making Changes

**Backend (API or Gradio):**
- Edit files in `src/`, `api.py`, or `app.py`
- Docker auto-reloads via volume mounts
- No need to rebuild!

**Frontend:**
- Edit files in `frontend/src/`
- Vite hot-reloads automatically
- Changes appear instantly in browser

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f gradio
docker-compose logs -f frontend
```

### Restarting Services

```bash
# Restart specific service
docker-compose restart api

# Rebuild after major changes
docker-compose up -d --build api
```

## 🌐 Running Without Docker (Alternative)

### Backend

```bash
# Terminal 1: API
./run_api.sh

# Terminal 2: Gradio
./run_ui.sh
```

### Frontend

```bash
# Terminal 3: Frontend
cd frontend
npm install
npm run dev
```

## 📋 Checklist

Before starting:
- [ ] `.env` file exists with API keys
- [ ] Docker Desktop is running
- [ ] Lovable code is exported and ready

Setting up Lovable:
- [ ] Extract Lovable code to `frontend/`
- [ ] Configure API URL in frontend code
- [ ] Uncomment frontend service in `docker-compose.yml`
- [ ] Run `docker-compose up -d --build`
- [ ] Visit http://localhost:5173

## 🐛 Common Issues

### "Port already in use"

```bash
# Kill processes on those ports
lsof -ti:8000 | xargs kill -9
lsof -ti:7860 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### "API connection failed" from frontend

1. Check API is running: `curl http://localhost:8000/`
2. Check CORS is enabled in `api.py`
3. Check API URL in frontend code

### "Docker build failed"

```bash
# Clean build
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### "Module not found" in frontend

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 Documentation

- **DOCKER_GUIDE.md** - Complete Docker reference
- **LOVABLE_INTEGRATION.md** - Detailed Lovable setup
- **UI_GUIDE.md** - Gradio UI documentation
- **frontend/README.md** - Frontend-specific guide

## 🎓 Architecture Overview

```
┌─────────────────────┐
│   Lovable Frontend  │
│   (React + Vite)    │
│   Port: 5173        │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│   FastAPI Backend   │
│   (REST API)        │
│   Port: 8000        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   CrewAI Agents     │
│   (4 specialists)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   OpenAI GPT-4o     │
└─────────────────────┘
```

Alternative simple UI:

```
┌─────────────────────┐
│   Gradio Web UI     │
│   Port: 7860        │
└──────────┬──────────┘
           │ Direct Python import
           ▼
┌─────────────────────┐
│   CrewAI Agents     │
└─────────────────────┘
```

## 🚀 Next Steps

1. **Test the current setup:**
   ```bash
   docker-compose up -d
   # Visit http://localhost:7860 and http://localhost:8000/docs
   ```

2. **Create your Lovable UI:**
   - Use the prompt from LOVABLE_INTEGRATION.md
   - Export and place in `frontend/`

3. **Launch your complete stack:**
   ```bash
   docker-compose up -d --build
   ```

4. **Start investigating MCP architectures!** 🎉

---

**Questions?** Check the detailed guides or logs:
```bash
docker-compose logs -f
```

Happy developing! 🚀
