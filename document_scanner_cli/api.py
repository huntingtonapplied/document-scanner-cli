"""Document Scanner API client — thin wrapper around httpx."""

import json
import os
import time
from typing import Any, Dict, Optional

import httpx

from document_scanner_cli.config import get_api_key, get_api_url, load_config
from document_scanner_cli.log import logger

MAX_RETRIES = int(os.getenv("DOCUMENT_SCANNER_MAX_RETRIES", "3"))
RETRY_BACKOFF_BASE = 1.0
RETRY_BACKOFF_MAX = 30.0
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
RETRYABLE_EXCEPTIONS = (httpx.ConnectError, httpx.TimeoutException)


_ERROR_HINTS = {
    401: ["Run: document-scanner login", "Or set DOCUMENT_SCANNER_API_KEY env var"],
    403: ["You may not have access to this resource."],
    404: ["The resource was not found.", "Run: document-scanner documents list"],
    422: ["The request data is invalid."],
    429: ["Rate limit exceeded."],
    500: ["Server error. Try again in a few minutes."],
}


def format_error_hint(status_code: int) -> str:
    hints = _ERROR_HINTS.get(status_code, [])
    if not hints:
        return ""
    return "\n".join(f"  {h}" for h in hints)


class AuthError(Exception):
    pass


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class DocumentScannerClient:
    """HTTP client for the Document Scanner API."""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        self.api_url = api_url or get_api_url()

        if not self.api_key:
            raise AuthError("Not authenticated.\n  Run: document-scanner login")

        config = load_config()
        self._timeout = float(os.getenv("DOCUMENT_SCANNER_TIMEOUT", config.get("timeout", 60)))
        self._client = httpx.Client(base_url=self.api_url, timeout=self._timeout)

    def _headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json", "Authorization": f"ApiKey {self.api_key}"}

    def _request_with_retry(self, method: str, path: str, **kwargs) -> httpx.Response:
        last_exc = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = getattr(self._client, method)(path, headers=self._headers(), **kwargs)
                if resp.status_code not in RETRYABLE_STATUS_CODES or attempt == MAX_RETRIES:
                    return resp
                delay = min(RETRY_BACKOFF_BASE * (2 ** attempt), RETRY_BACKOFF_MAX)
                time.sleep(delay)
            except RETRYABLE_EXCEPTIONS as exc:
                last_exc = exc
                if attempt == MAX_RETRIES:
                    raise
                time.sleep(min(RETRY_BACKOFF_BASE * (2 ** attempt), RETRY_BACKOFF_MAX))
        raise last_exc or APIError("Request failed after retries")

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("get", path, params=params)
        return self._handle_response(resp)

    def post(self, path: str, data: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("post", path, json=data)
        return self._handle_response(resp)

    def put(self, path: str, data: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("put", path, json=data)
        return self._handle_response(resp)

    def delete(self, path: str) -> Any:
        resp = self._request_with_retry("delete", path)
        if resp.status_code == 204:
            return None
        return self._handle_response(resp)

    def _handle_response(self, resp: httpx.Response) -> Any:
        if resp.status_code == 401:
            raise AuthError("Not authenticated.")
        if resp.status_code >= 400:
            detail = ""
            try:
                body = resp.json()
                detail = body.get("detail", resp.text)
            except Exception:
                detail = resp.text
            hint = format_error_hint(resp.status_code)
            msg = f"API error {resp.status_code}: {detail}"
            if hint:
                msg += f"\n{hint}"
            raise APIError(msg, status_code=resp.status_code)
        return resp.json()

    # Document operations
    def list_documents(self, params: Optional[Dict] = None) -> list:
        data = self.get("/v1/documents", params=params)
        return data.get("data", data) if isinstance(data, dict) else data

    def get_document(self, document_id: str) -> dict:
        return self.get(f"/v1/documents/{document_id}")

    def upload_document(self, data: dict) -> dict:
        return self.post("/v1/documents/upload", data)

    def delete_document(self, document_id: str) -> None:
        self.delete(f"/v1/documents/{document_id}")

    # Scanner operations
    def init_scan(self, data: dict) -> dict:
        return self.post("/v1/scanner/init", data)

    def get_scan_status(self, scan_id: str) -> dict:
        return self.get(f"/v1/scanner/status/{scan_id}")

    # Sync operations
    def get_sync_status(self) -> dict:
        return self.get("/v1/sync/status")

    def trigger_sync(self, data: Optional[dict] = None) -> dict:
        return self.post("/v1/sync/trigger", data or {})

    def get_sync_settings(self) -> dict:
        return self.get("/v1/sync/settings")

    def update_sync_settings(self, data: dict) -> dict:
        return self.put("/v1/sync/settings", data)

    # Metrics operations
    def get_metrics_counts(self) -> dict:
        return self.get("/v1/metrics/counts")

    def get_metrics_documents(self) -> dict:
        return self.get("/v1/metrics/documents")

    def get_dashboard(self) -> dict:
        return self.get("/v1/metrics/dashboard")

    # User operations
    def get_current_user(self) -> dict:
        return self.get("/v1/auth/me")
