# FlatPDF API — Deployment Guide

## Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.12+ (for local dev without Docker)

### Option 1: Docker Compose (Recommended)

```bash
# Clone and navigate
cd /home/zzy/auto-company/projects/flatpdf-api

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Test API
curl http://localhost:8000/health
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Start Gotenberg separately
docker run -p 3000:3000 gotenberg/gotenberg:8

# Run API
GOTENBERG_URL=http://localhost:3000 uvicorn src.main:app --reload
```

## Production Deployment

### Railway Deploy

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd /home/zzy/auto-company/projects/flatpdf-api
railway init

# Deploy
railway up

# Add Gotenberg service
railway add --service gotenberg
railway variables set GOTENBERG_IMAGE=gotenberg/gotenberg:8
```

### Environment Variables

| Variable | Value |
|----------|-------|
| GOTENBERG_URL | Gotenberg service URL |
| API_KEY | Random secret key |
| PORT | 8000 (Railway sets this) |

## API Usage

```bash
# Health check
curl https://your-api.railway.app/health

# Convert HTML to PDF
curl -X POST https://your-api.railway.app/convert \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<h1>Hello World</h1>"
  }'
```

## Monitoring

- Railway Dashboard: https://railway.app
- API Docs: https://your-api.railway.app/docs
- Metrics: Built-in Railway metrics

---

*Auto Company — Cycle #51*
*FlatPDF API — Deployment Guide*
