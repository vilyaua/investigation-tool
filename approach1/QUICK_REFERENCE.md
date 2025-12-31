# Quick Reference Card

## 🎯 Lovable Code Location

```
frontend/   ← PUT YOUR LOVABLE CODE HERE
```

## 🚀 Docker Commands

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Rebuild service
docker-compose up -d --build <service>
```

## 🌐 Service URLs

| Service | URL |
|---------|-----|
| Gradio | http://localhost:7860 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Frontend | http://localhost:5173 |

## 📝 Local Development (No Docker)

```bash
# Terminal 1: API
./run_api.sh

# Terminal 2: Gradio
./run_ui.sh

# Terminal 3: Frontend
cd frontend && npm run dev
```

## 🔑 Environment Setup

```bash
# Copy template
cp .env.example .env

# Edit with your keys
nano .env
```

Required:
- `OPENAI_API_KEY`

Optional:
- `SERPER_API_KEY`

## 📦 Lovable Setup Steps

1. Export from Lovable.dev
2. Extract to `frontend/`
3. Configure API URL
4. Uncomment frontend in `docker-compose.yml`
5. Run: `docker-compose up -d --build`

## 📚 Documentation

- `SETUP_SUMMARY.md` - Overview & workflow
- `DOCKER_GUIDE.md` - Complete Docker guide
- `LOVABLE_INTEGRATION.md` - Lovable setup
- `frontend/README.md` - Frontend guide

## 🐛 Troubleshooting

```bash
# Port in use
lsof -ti:8000 | xargs kill -9

# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check service health
docker-compose ps
curl http://localhost:8000/
```

## 🎓 Project Structure

```
investigation-tool/
├── frontend/        ← Lovable code here
├── src/            ← Backend Python
├── api.py          ← REST API
├── app.py          ← Gradio UI
└── docker-compose.yml
```
