# FlatPDF API

> **Self-hosted HTML to PDF conversion API. Simple. Fast. Yours.**

FlatPDF is a REST API that converts HTML to PDF. Unlike cloud services that charge per conversion and lock you in, FlatPDF is designed to be **self-hosted** — run it on your own server, control your data, pay nothing per conversion.

## Why FlatPDF?

| Problem | FlatPDF Solution |
|---------|------------------|
| Cloud APIs charge $0.01-0.10 per page | **Free forever** when self-hosted |
| Data leaves your infrastructure | **Your server, your data** |
| Monthly subscriptions add up | **One-time setup, zero ongoing cost** |
| Vendor lock-in | **Open source, Docker-based, portable** |

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
git clone https://github.com/ozxc44/flatpdf-api.git
cd flatpdf-api
docker compose up -d
```

That's it! Your API is running at `http://localhost:8000`

### Option 2: Docker

```bash
docker run -d \
  -p 8000:8000 \
  -e GOTENBERG_URL=http://gotenberg:3000 \
  ghcr.io/ozxc44/flatpdf:latest
```

## API Usage

### Convert HTML to PDF

```bash
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "html": "<h1>Invoice #123</h1><p>Amount: $99.00</p>",
    "options": {
      "format": "A4",
      "margin": "1cm"
    }
  }'
```

### Convert URL to PDF

```bash
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "url": "https://example.com/invoice.html"
  }'
```

### Response

```json
{
  "success": true,
  "pdf_base64": "JVBERi0xLjcK...",
  "pages": 1
}
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GOTENBERG_URL` | `http://gotenberg:3000` | Gotenberg service URL |
| `API_KEY` | `dev-key-change-me` | API authentication key |

## Deploy Anywhere

Since FlatPDF is containerized, you can deploy it anywhere Docker runs:

- **Your server**: AWS, DigitalOcean, Linode, Hetzner
- **PaaS**: Railway, Render, Fly.io
- **Kubernetes**: Use provided Helm chart (coming soon)
- **Local**: Development and testing

## Tech Stack

- **FastAPI** — Modern Python API framework
- **Gotenberg** — Docker-based Chromium for PDF generation
- **Docker** — Containerization for easy deployment

## Use Cases

- **Invoices & Receipts** — E-commerce platforms
- **Contracts** — SaaS agreement generation
- **Certificates** — Course completion badges
- **Reports** — Analytics dashboards export
- **Labels** — Shipping and logistics

## Production Checklist

- [ ] Change default `API_KEY`
- [ ] Enable HTTPS (use reverse proxy like Caddy/Nginx)
- [ ] Set resource limits on containers
- [ ] Configure backup strategy
- [ ] Set up monitoring

## Roadmap

- [ ] Streaming PDF responses
- [ ] Webhook notifications
- [ ] Template engine integration
- [ ] AWS Lambda support
- [ ] Batch conversion API

## License

MIT — Use it however you want. Commercial, personal, open source — all fine.

## Support

- GitHub Issues: [github.com/ozxc44/flatpdf-api/issues](https://github.com/ozxc44/flatpdf-api/issues)
- Documentation: [docs.flatpdf.io](https://docs.flatpdf.io) (coming soon)

---

**FlatPDF** — Your PDFs, your infrastructure, your rules.

*Auto Company — Cycle #52*
