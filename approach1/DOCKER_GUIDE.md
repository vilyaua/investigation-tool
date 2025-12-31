# Docker Development Guide

Complete guide for running the MCP Investigation Tool with Docker.

## Project Structure

```
investigation-tool/
├── docker-compose.yml       # Orchestrates all services
├── Dockerfile.api           # FastAPI backend
├── Dockerfile.gradio        # Gradio UI
├── frontend/
│   ├── Dockerfile          # Lovable frontend
│   └── (your Lovable code here)
├── src/                    # Python source code
├── outputs/                # Shared investigation reports
└── .env                    # Environment variables
```

## Quick Start

### 1. Prerequisites

- Docker Desktop installed
- `.env` file with API keys

### 2. Start All Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### 3. Access Services

- **Gradio UI:** http://localhost:7860
- **FastAPI:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173 (after adding Lovable code)

## Individual Services

### Run API Only

```bash
docker-compose up api
```

### Run Gradio UI Only

```bash
docker-compose up gradio
```

### Run Frontend Only (after setup)

```bash
docker-compose up frontend
```

## Development Workflow

### Initial Setup

1. **Clone and configure:**
   ```bash
   git clone <repo>
   cd investigation-tool
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Build all services:**
   ```bash
   docker-compose build
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

### Adding Lovable Frontend

1. **Export your Lovable project:**
   - In Lovable.dev, export your project
   - Download the ZIP file

2. **Extract to frontend directory:**
   ```bash
   cd investigation-tool
   unzip lovable-export.zip -d frontend/
   ```

3. **Update API URL in frontend:**

   Edit `frontend/src/lib/api.ts` or equivalent:
   ```typescript
   const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   ```

4. **Enable frontend in docker-compose.yml:**

   Uncomment the frontend service:
   ```yaml
   frontend:
     build:
       context: ./frontend
       dockerfile: Dockerfile
     # ... rest of config
   ```

5. **Rebuild and start:**
   ```bash
   docker-compose up -d --build frontend
   ```

### Hot Reload Development

All services have volume mounts for hot reloading:

- **API:** Changes to `src/` or `api.py` restart automatically
- **Gradio:** Changes to `src/` or `app.py` restart automatically
- **Frontend:** Changes to `frontend/src/` hot reload in browser

```bash
# Watch logs while developing
docker-compose logs -f api
docker-compose logs -f gradio
docker-compose logs -f frontend
```

## Common Commands

### View Service Status

```bash
docker-compose ps
```

### Restart a Service

```bash
docker-compose restart api
docker-compose restart gradio
docker-compose restart frontend
```

### Rebuild After Changes

```bash
# Rebuild specific service
docker-compose build api

# Rebuild and restart
docker-compose up -d --build api
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail=100 api
```

### Execute Commands in Container

```bash
# Open shell in API container
docker-compose exec api bash

# Run a Python script
docker-compose exec api python -c "print('Hello')"

# Install a package
docker-compose exec api pip install new-package
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove volumes too (deletes outputs)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Environment Variables

Create a `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional but recommended
SERPER_API_KEY=...

# Frontend (if using)
VITE_API_URL=http://localhost:8000
```

## Production Deployment

### Build Production Images

```bash
# Build optimized images
docker-compose -f docker-compose.prod.yml build

# Push to registry
docker tag mcp-investigation-api:latest your-registry/mcp-api:latest
docker push your-registry/mcp-api:latest
```

### Deploy to Cloud

#### Docker Compose (Simple)

```bash
# On your server
git clone <repo>
cd investigation-tool
cp .env.example .env
# Edit .env with production keys

docker-compose up -d
```

#### Kubernetes (Advanced)

See `k8s/` directory for Kubernetes manifests (if you need this, let me know).

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -ti:8000 | xargs kill -9
lsof -ti:7860 | xargs kill -9
lsof -ti:5173 | xargs kill -9

# Or change ports in docker-compose.yml
```

### Container Won't Start

```bash
# Check logs
docker-compose logs api

# Rebuild from scratch
docker-compose build --no-cache api
docker-compose up api
```

### API Connection Failed

```bash
# Check API is running
curl http://localhost:8000/

# Check from inside frontend container
docker-compose exec frontend curl http://api:8000/
```

### Permission Issues

```bash
# Fix outputs directory permissions
sudo chown -R $USER:$USER outputs/
chmod -R 755 outputs/
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a

# Remove unused volumes
docker volume prune
```

## Performance Optimization

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Multi-Stage Builds

For smaller images, use multi-stage builds (already optimized).

### Caching

Docker caches layers - order your Dockerfile to maximize cache hits:
1. Copy requirements first
2. Install dependencies
3. Copy source code last

## Monitoring

### Health Checks

All services have health checks:

```bash
# View health status
docker-compose ps
```

### Logs

```bash
# Export logs
docker-compose logs > logs.txt

# Filter logs
docker-compose logs api | grep ERROR
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Docker Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build images
        run: docker-compose build
      - name: Run tests
        run: docker-compose up -d && sleep 10 && curl http://localhost:8000/
```

## Network Configuration

Services communicate via Docker network:

- Frontend → API: `http://api:8000`
- Gradio → API: Can import directly (same codebase)

External access uses `localhost:PORT`.

## Data Persistence

### Outputs Volume

Investigation reports persist in `./outputs` directory:

```yaml
volumes:
  - ./outputs:/app/outputs
```

Even if you `docker-compose down`, reports remain.

### Database (Future)

To add persistent database:

```yaml
services:
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Tips

1. **Use named volumes for production**
2. **Never commit .env to git**
3. **Use docker-compose.override.yml for local customization**
4. **Enable BuildKit for faster builds:**
   ```bash
   export DOCKER_BUILDKIT=1
   export COMPOSE_DOCKER_CLI_BUILD=1
   ```
5. **Use .dockerignore to exclude files:**
   ```
   venv/
   __pycache__/
   *.pyc
   .git/
   ```

## Next Steps

1. ✅ Services are configured
2. 📦 Add your Lovable code to `frontend/`
3. 🚀 Run `docker-compose up -d`
4. 🎉 Develop with hot reload!

---

Need help? Check logs with `docker-compose logs -f`
