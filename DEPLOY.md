# FlatPDF API — Deployment Guide

## Quick Start: Docker Compose

```bash
git clone https://github.com/ozxc44/flatpdf-api.git
cd flatpdf-api
docker compose up -d
```

That's it! API running at `http://localhost:8000`

Test it:
```bash
curl http://localhost:8000/health
```

---

## Production Deployment

### Option 1: Railway (Easiest)

1. Fork this repo
2. Import to Railway
3. Railway auto-detects Docker
4. Set `GOTENBERG_URL` to Gotenberg service

### Option 2: Render

1. Fork this repo
2. Create Web Service
3. Render builds and deploys

### Option 3: Your VPS (Cheapest)

```bash
# Clone
git clone https://github.com/ozxc44/flatpdf-api.git
cd flatpdf-api

# Set environment
cp .env.example .env
nano .env  # Edit API_KEY

# Deploy
docker compose up -d
```

### Option 4: Kubernetes

```bash
kubectl apply -f k8s/
```

---

## Security Checklist

- [ ] Set strong `API_KEY` (run `openssl rand -hex 32`)
- [ ] Enable HTTPS (use Caddy for automatic HTTPS)
- [ ] Set rate limits
- [ ] Configure firewall

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GOTENBERG_URL` | `http://gotenberg:3000` | Gotenberg service URL |
| `API_KEY` | `dev-key-change-me` | **Must change in production** |

---

## Troubleshooting

**Gotenberg unreachable?**
```bash
docker ps | grep gotenberg
curl http://localhost:3000/health
```

**Out of memory?**
Gotenberg needs ~500MB RAM. Check your server specs.

---

*Auto Company — Cycle #52*
