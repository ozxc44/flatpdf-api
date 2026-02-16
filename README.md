# FlatPDF API

> Simple, fast, affordable HTML to PDF conversion API.

## Overview

FlatPDF is a REST API that converts HTML to PDF. Designed for developers who need to generate invoices, contracts, certificates, and reports without the headache of maintaining Puppeteer infrastructure.

## Features

- Convert HTML string or URL to PDF
- High-quality PDF output with modern CSS support
- Simple REST API
- Fair pricing: $9/month or $49 lifetime
- 100 free conversions/month

## API Endpoints

### POST /convert

Convert HTML to PDF.

**Request:**
```json
{
  "html": "<html><body><h1>Hello World</h1></body></html>",
  "options": {
    "format": "A4",
    "margin": "1cm"
  }
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://cdn.flatpdf.io/files/xxx.pdf",
  "pages": 1
}
```

## Pricing

| Plan | Price | Conversions |
|------|-------|-------------|
| Free | $0 | 100/month |
| Pro | $9/month | Unlimited |
| Lifetime | $49 once | Unlimited |

## Quick Start

```bash
curl -X POST https://api.flatpdf.io/convert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"html": "<h1>Hello</h1>"}'
```

## Status

🚧 In Development - Coming soon to RapidAPI

---

*Auto Company — Cycle #51*
