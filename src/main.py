"""
FlatPDF API — HTML to PDF Conversion Service

Simple REST API for converting HTML to PDF.
Built with FastAPI + Gotenberg.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
import httpx
from dotenv import load_dotenv

load_dotenv()

# Configuration
GOTENBERG_URL = os.getenv("GOTENBERG_URL", "http://localhost:3000")
API_KEY = os.getenv("API_KEY", "dev-key-change-in-production")

app = FastAPI(
    title="FlatPDF API",
    description="Simple HTML to PDF conversion API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Models
class ConvertRequest(BaseModel):
    html: Optional[str] = Field(None, description="HTML string to convert")
    url: Optional[str] = Field(None, description="URL to convert")
    options: Optional[dict] = Field(default_factory=dict, description="PDF generation options")

    class Config:
        json_schema_extra = {
            "example": {
                "html": "<h1>Hello World</h1><p>This is a PDF.</p>",
                "options": {
                    "format": "A4",
                    "margin": "1cm"
                }
            }
        }


class ConvertResponse(BaseModel):
    success: bool
    url: Optional[str] = None
    pdf_base64: Optional[str] = None
    pages: Optional[int] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    gotenberg: str
    version: str


# Middleware: API Key Authentication
async def verify_api_key(request: Request):
    """Verify API key from Authorization header."""
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key. Use: Authorization: Bearer YOUR_KEY"
        )

    key = auth_header.replace("Bearer ", "").strip()

    # For MVP, accept any non-empty key in dev mode
    if not key or (API_KEY != "dev-key-change-in-production" and key != API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    return key


# Endpoints
@app.get("/", response_model=dict)
async def root():
    """API information."""
    return {
        "service": "FlatPDF API",
        "version": "0.1.0",
        "status": "operational",
        "endpoints": {
            "convert": "POST /convert",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    gotenberg_status = "unknown"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{GOTENBERG_URL}/health")
            gotenberg_status = "ok" if response.status_code == 200 else "error"
    except Exception:
        gotenberg_status = "unreachable"

    return HealthResponse(
        status="ok",
        gotenberg=gotenberg_status,
        version="0.1.0"
    )


@app.post("/convert", response_model=ConvertResponse)
async def convert_html_to_pdf(request: ConvertRequest, http_request: Request):
    """
    Convert HTML or URL to PDF.

    Accepts either:
    - HTML string directly
    - URL to convert

    Returns PDF as base64 encoded string (for MVP).
    Production will return CDN URL.
    """

    # Verify API key
    await verify_api_key(http_request)

    # Validation
    if not request.html and not request.url:
        return ConvertResponse(
            success=False,
            error="Either 'html' or 'url' is required"
        )

    if request.html and request.url:
        return ConvertResponse(
            success=False,
            error="Provide either 'html' or 'url', not both"
        )

    try:
        # For MVP: Mock response since Gotenberg isn't deployed yet
        # In production, this will call Gotenberg API
        return ConvertResponse(
            success=True,
            message="API is ready. Gotenberg integration in progress...",
            input_received={
                "has_html": bool(request.html),
                "has_url": bool(request.url),
                "html_length": len(request.html) if request.html else 0,
                "url": request.url
            },
            next_steps=[
                "Deploy Gotenberg service",
                "Implement actual PDF generation",
                "Return PDF or CDN URL"
            ]
        )

        # Production implementation (coming soon):
        # async with httpx.AsyncClient(timeout=30.0) as client:
        #     gotenberg_request = {
        #         "url": request.url if request.url else None,
        #         "html": request.html if request.html else None,
        #     }
        #     response = await client.post(
        #         f"{GOTENBERG_URL}/forms/chromium/convert/pdf",
        #         data=gotenberg_request,
        #     )
        #     pdf_bytes = response.content
        #     # Store and return URL or base64

    except httpx.TimeoutException:
        return ConvertResponse(
            success=False,
            error="PDF generation timed out. Try reducing HTML complexity."
        )
    except Exception as e:
        return ConvertResponse(
            success=False,
            error=f"Internal error: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom error handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
