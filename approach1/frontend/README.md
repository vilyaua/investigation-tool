# Frontend Directory

This directory is for your Lovable.dev frontend code.

## Setup Instructions

### 1. Export from Lovable.dev

1. Go to your Lovable project
2. Click the export button
3. Download the ZIP file

### 2. Extract Here

```bash
# From the investigation-tool root directory
cd frontend

# Extract your Lovable export
unzip ~/Downloads/lovable-export.zip -d .

# Or manually copy files:
# - src/
# - public/
# - package.json
# - etc.
```

### 3. Expected Structure

After extraction, this directory should look like:

```
frontend/
├── src/
│   ├── components/
│   ├── lib/
│   ├── pages/
│   └── main.tsx
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── Dockerfile (already here)
└── README.md (this file)
```

### 4. Configure API Connection

Update the API URL in your code:

**Option A: Environment Variable (Recommended)**

Create `frontend/.env`:
```bash
VITE_API_URL=http://localhost:8000
```

Then in your code:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

**Option B: Direct in Code**

Edit `src/lib/api.ts` or equivalent:
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### 5. Run Locally (Without Docker)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Visit http://localhost:5173

### 6. Run with Docker

From the root directory:

```bash
# Edit docker-compose.yml and uncomment the frontend service

# Then run:
docker-compose up -d frontend
```

Visit http://localhost:5173

## Development

### Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

### Docker Development

```bash
# Build and run
docker-compose up frontend

# Rebuild after changes
docker-compose up -d --build frontend

# View logs
docker-compose logs -f frontend
```

## API Integration

Your frontend should connect to these endpoints:

- **POST** `/api/investigate` - Start investigation
- **GET** `/api/status/{topic}` - Check status
- **GET** `/api/recent` - List recent investigations
- **GET** `/api/report/{filename}` - Get specific report

See [../LOVABLE_INTEGRATION.md](../LOVABLE_INTEGRATION.md) for detailed API documentation.

## Tips

1. **CORS is already enabled** in the API for local development
2. **Hot reload works** with Docker volumes
3. **Use Vite environment variables** for configuration
4. **Check API health** at http://localhost:8000/docs

## Troubleshooting

### API Connection Failed

```bash
# Check API is running
curl http://localhost:8000/

# From inside Docker
docker-compose exec frontend curl http://api:8000/
```

### Port 5173 Already in Use

Change port in `vite.config.ts`:
```typescript
export default {
  server: {
    port: 3000 // or any other port
  }
}
```

### Build Fails

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. Export your Lovable project
2. Extract files to this directory
3. Configure API URL
4. Run with `docker-compose up frontend`
5. Start developing!

---

**Note:** The `.gitkeep` file can be deleted once you add your Lovable code.
