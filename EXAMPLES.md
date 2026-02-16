# FlatPDF API — Integration Examples

Quick integration examples for common programming languages and frameworks.

## Quick Start

```bash
docker run -d -p 8000:8000 ghcr.io/ozxc44/flatpdf-api:latest
```

The API will be available at `http://localhost:8000`

---

## cURL

### Convert HTML to PDF

```bash
curl -X POST http://localhost:8000/api/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<h1>Hello, World!</h1><p>This is a PDF.</p>"
  }' \
  --output output.pdf
```

### Convert URL to PDF

```bash
curl -X POST http://localhost:8000/api/pdf/from-url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }' \
  --output output.pdf
```

### With Options

```bash
curl -X POST http://localhost:8000/api/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<h1>Invoice #1234</h1>",
    "options": {
      "format": "A4",
      "margin_top": "20px",
      "margin_bottom": "20px",
      "print_background": true
    }
  }' \
  --output invoice.pdf
```

---

## Python

### Using requests

```python
import requests

API_URL = "http://localhost:8000/api/pdf"

def generate_pdf(html_content):
    response = requests.post(
        API_URL,
        json={"html": html_content}
    )
    response.raise_for_status()
    return response.content

# Usage
html = "<h1>Invoice</h1><p>Amount: $99.00</p>"
pdf_bytes = generate_pdf(html)

with open("invoice.pdf", "wb") as f:
    f.write(pdf_bytes)
```

### With options

```python
def generate_pdf_with_options(html_content, filename="output.pdf"):
    response = requests.post(
        API_URL,
        json={
            "html": html_content,
            "options": {
                "format": "A4",
                "margin": {"top": "20px", "bottom": "20px"},
                "print_background": True
            }
        }
    )
    response.raise_for_status()

    with open(filename, "wb") as f:
        f.write(response.content)
```

### FastAPI Integration

```python
from fastapi import FastAPI, Response
import requests

app = FastAPI()
PDF_API = "http://localhost:8000/api/pdf"

@app.post("/generate-invoice")
async def generate_invoice(invoice_data: dict):
    html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial; }}
                h1 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>Invoice #{invoice_data['number']}</h1>
            <p>Total: ${invoice_data['total']}</p>
        </body>
    </html>
    """

    pdf_response = requests.post(PDF_API, json={"html": html})
    return Response(content=pdf_response.content, media_type="application/pdf")
```

---

## JavaScript / Node.js

### Using fetch

```javascript
const API_URL = 'http://localhost:8000/api/pdf';

async function generatePDF(html) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ html })
  });

  if (!response.ok) throw new Error('PDF generation failed');

  return await response.buffer();
}

// Usage with fs
const fs = require('fs');

const html = '<h1>Hello World</h1>';
generatePDF(html).then(pdf => {
  fs.writeFileSync('output.pdf', pdf);
});
```

### Express.js Integration

```javascript
const express = require('express');
const fetch = require('node-fetch');

const app = express();
const PDF_API = 'http://localhost:8000/api/pdf';

app.post('/api/invoice', async (req, res) => {
  const html = `
    <html>
      <body>
        <h1>Invoice #${req.body.number}</h1>
        <p>Total: $${req.body.total}</p>
      </body>
    </html>
  `;

  const pdfResponse = await fetch(PDF_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ html })
  });

  const pdf = await pdfResponse.buffer();
  res.setHeader('Content-Type', 'application/pdf');
  res.send(pdf);
});

app.listen(3000);
```

### Next.js API Route

```javascript
// pages/api/generate-pdf.js

export default async function handler(req, res) {
  const { html } = req.body;

  const pdfResponse = await fetch('http://localhost:8000/api/pdf', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ html })
  });

  const pdf = await pdfResponse.arrayBuffer();

  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', 'attachment; filename="document.pdf"');
  res.send(Buffer.from(pdf));
}
```

---

## Go

```go
package main

import (
    "bytes"
    "io"
    "net/http"
    "os"
)

const PDF_API = "http://localhost:8000/api/pdf"

func generatePDF(html string) ([]byte, error) {
    payload := []byte(`{"html": "` + html + `"}`)

    resp, err := http.Post(PDF_API, "application/json", bytes.NewBuffer(payload))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    return io.ReadAll(resp.Body)
}

func main() {
    html := "<h1>Hello from Go!</h1>"
    pdf, err := generatePDF(html)
    if err != nil {
        panic(err)
    }

    os.WriteFile("output.pdf", pdf, 0644)
}
```

---

## Ruby

```ruby
require 'net/http'
require 'uri'
require 'json'

PDF_API = 'http://localhost:8000/api/pdf'

def generate_pdf(html)
  uri = URI(PDF_API)
  req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
  req.body = { html: html }.to_json

  response = Net::HTTP.start(uri.hostname, uri.port) do |http|
    http.request(req)
  end

  response.body
end

# Usage
html = '<h1>Hello from Ruby!</h1>'
pdf = generate_pdf(html)
File.write('output.pdf', pdf)
```

---

## PHP

```php
<?php

function generatePDF($html) {
    $api_url = 'http://localhost:8000/api/pdf';

    $data = json_encode(['html' => $html]);

    $options = [
        'http' => [
            'method'  => 'POST',
            'header'  => 'Content-Type: application/json',
            'content' => $data
        ]
    ];

    $context  = stream_context_create($options);
    return file_get_contents($api_url, false, $context);
}

// Usage
$html = '<h1>Hello from PHP!</h1>';
$pdf = generatePDF($html);
file_put_contents('output.pdf', $pdf);
?>
```

---

## Docker Compose (Multi-Service)

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    environment:
      - PDF_API_URL=http://flatpdf:8000
    depends_on:
      - flatpdf

  flatpdf:
    image: ghcr.io/ozxc44/flatpdf-api:latest
    ports:
      - "8000:8000"
```

---

## Common Use Cases

### Invoice Generation

```python
def create_invoice(client_name, items):
    html = f"""
    <html>
        <style>
            .invoice {{ font-family: Arial; padding: 40px; }}
            .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; }}
            .items {{ margin-top: 30px; }}
            .item {{ display: flex; justify-content: space-between; }}
        </style>
        <body class="invoice">
            <div class="header">
                <h1>Invoice</h1>
                <p>Client: {client_name}</p>
            </div>
            <div class="items">
    """

    for item in items:
        html += f'<div class="item"><span>{item["name"]}</span><span>${item["price"]}</span></div>'

    html += "</div></body></html>"
    return generate_pdf(html)
```

### Report Generation

```python
def generate_report(data):
    html = f"""
    <html>
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="container mt-4">
            <h1>Monthly Report</h1>
            <table class="table table-striped">
                <thead><tr><th>Metric</th><th>Value</th></tr></thead>
                <tbody>
    """

    for key, value in data.items():
        html += f"<tr><td>{key}</td><td>{value}</td></tr>"

    html += "</tbody></table></body></html>"
    return generate_pdf(html)
```

### Label/Receipt Printing

```python
def generate_shipping_label(order):
    html = f"""
    <html>
        <style>
            .label {{ width: 4in; height: 6in; padding: 20px; }}
            .barcode {{ font-size: 40px; text-align: center; }}
        </style>
        <body class="label">
            <h1>SHIPPING LABEL</h1>
            <div class="barcode">*{order['tracking_number']}*</div>
            <p><strong>To:</strong> {order['address']}</p>
        </body>
    </html>
    """
    return generate_pdf(html)
```

---

## Testing

```bash
# Test the API is running
curl http://localhost:8000/

# Generate a simple test PDF
curl -X POST http://localhost:8000/api/pdf \
  -H "Content-Type: application/json" \
  -d '{"html": "<h1>Test PDF</h1>"}' \
  --output test.pdf
```

---

## Troubleshooting

### Connection Refused
- Ensure the container is running: `docker ps`
- Check the port is correct: `-p 8000:8000`

### Timeout on Large HTML
- Increase timeout in your HTTP client
- Consider simplifying the HTML or removing external resources

### PDF Layout Issues
- Ensure CSS is inline or in `<style>` tags
- External stylesheets may not load in self-hosted environments
- Test with simple HTML first to isolate the issue

---

## Need Help?

- GitHub Issues: https://github.com/ozxc44/flatpdf-api/issues
- Documentation: https://github.com/ozxc44/flatpdf-api#readme
