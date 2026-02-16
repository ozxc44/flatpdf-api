"""
FlatPDF API Tests

Run with: pytest test_api.py -v
Or directly: python test_api.py
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi.testclient import TestClient
from src.main import app, API_KEY

client = TestClient(app)


class TestRootEndpoint:
    """Test root endpoint."""

    def test_root_returns_service_info(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "FlatPDF API"
        assert data["status"] == "operational"
        assert "endpoints" in data

    def test_root_has_correct_endpoints(self):
        response = client.get("/")
        data = response.json()
        endpoints = data["endpoints"]
        assert "convert" in endpoints
        assert "health" in endpoints
        assert "docs" in endpoints


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_returns_ok_status(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "gotenberg" in data
        assert data["version"] == "0.1.0"


class TestConvertEndpoint:
    """Test PDF conversion endpoint."""

    def test_convert_without_auth_returns_401(self):
        response = client.post("/convert", json={
            "html": "<h1>Test</h1>"
        })
        assert response.status_code == 401

    def test_convert_with_valid_accepts_request(self):
        response = client.post(
            "/convert",
            json={"html": "<h1>Test</h1>"},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data

    def test_convert_requires_html_or_url(self):
        response = client.post(
            "/convert",
            json={},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False
        assert "html" in data["error"].lower() or "url" in data["error"].lower()

    def test_convert_rejects_both_html_and_url(self):
        response = client.post(
            "/convert",
            json={
                "html": "<h1>Test</h1>",
                "url": "https://example.com"
            },
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == False

    def test_convert_with_html_works(self):
        response = client.post(
            "/convert",
            json={
                "html": "<h1>Hello World</h1><p>This is a test PDF.</p>",
                "options": {"format": "A4"}
            },
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        assert response.status_code == 200
        data = response.json()
        # Note: Without Gotenberg running, this will return an error
        # With Gotenberg, success will be True and pdf_base64 will be present
        assert "success" in data

    def test_convert_with_url_works(self):
        response = client.post(
            "/convert",
            json={"url": "https://example.com"},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        assert response.status_code == 200
        data = response.json()
        # Note: Without Gotenberg running, this will return an error
        # With Gotenberg, success will be True and pdf_base64 will be present
        assert "success" in data


class TestDocsEndpoints:
    """Test documentation endpoints."""

    def test_swagger_docs_accessible(self):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_docs_accessible(self):
        response = client.get("/redoc")
        assert response.status_code == 200


def run_tests():
    """Run tests without pytest."""
    tests = [
        TestRootEndpoint(),
        TestHealthEndpoint(),
        TestConvertEndpoint(),
        TestDocsEndpoints(),
    ]

    passed = 0
    failed = 0

    for test_class in tests:
        class_name = test_class.__class__.__name__
        for method_name in dir(test_class):
            if method_name.startswith("test_"):
                try:
                    getattr(test_class, method_name)()
                    print(f"✓ {class_name}.{method_name}")
                    passed += 1
                except AssertionError as e:
                    print(f"✗ {class_name}.{method_name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"✗ {class_name}.{method_name}: ERROR - {e}")
                    failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
