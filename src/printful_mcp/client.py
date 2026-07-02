"""Shared Printful API client with authentication and error handling."""

import os
import json
from typing import Any, Dict, Optional
import httpx


class PrintfulAPIError(Exception):
    """Base exception for Printful API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, detail: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


class PrintfulClient:
    """Async HTTP client for Printful API v2 and v1."""
    
    def __init__(self, api_key: Optional[str] = None, store_id: Optional[str] = None):
        """
        Initialize Printful API client.
        
        Args:
            api_key: Printful OAuth API key (defaults to PRINTFUL_API_KEY env var)
            store_id: Optional store ID for account-level tokens (defaults to PRINTFUL_STORE_ID env var)
        """
        self.api_key = api_key or os.getenv("PRINTFUL_API_KEY")
        if not self.api_key:
            raise ValueError("PRINTFUL_API_KEY environment variable or api_key parameter is required")
        
        self.store_id = store_id or os.getenv("PRINTFUL_STORE_ID")
        self.base_url_v2 = "https://api.printful.com/v2"
        self.base_url_v1 = "https://api.printful.com"
        
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
    
    def _get_headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Get request headers with optional store ID and extra headers."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if self.store_id:
            headers["X-PF-Store-Id"] = self.store_id
        
        if extra_headers:
            headers.update(extra_headers)
        
        return headers
    
    async def request(
        self,
        method: str,
        endpoint: str,
        version: str = "v2",
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to Printful API.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (e.g., "/catalog-products")
            version: API version ("v2" or "v1")
            params: Query parameters
            json_data: JSON request body
            extra_headers: Additional headers
        
        Returns:
            Response data as dict
        
        Raises:
            PrintfulAPIError: On API errors
        """
        base_url = self.base_url_v2 if version == "v2" else self.base_url_v1
        url = f"{base_url}{endpoint}"
        headers = self._get_headers(extra_headers)
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers,
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "60")
                raise PrintfulAPIError(
                    f"Rate limit exceeded. Retry after {retry_after} seconds.",
                    status_code=429,
                    detail={"retry_after": retry_after}
                )
            
            # Handle successful responses
            if 200 <= response.status_code < 300:
                # v2 API returns JSON directly
                if version == "v2":
                    return response.json()
                # v1 API wraps response in {"code": ..., "result": ...}
                else:
                    data = response.json()
                    return data.get("result", data)
            
            # Handle error responses
            await self._handle_error(response, version)
            
        except httpx.TimeoutException:
            raise PrintfulAPIError("Request timed out. Please try again.")
        except httpx.RequestError as e:
            raise PrintfulAPIError(f"Request error: {str(e)}")
        except json.JSONDecodeError:
            raise PrintfulAPIError(f"Invalid JSON response from API (status {response.status_code})")
    
    async def _handle_error(self, response: httpx.Response, version: str) -> None:
        """Handle API error responses."""
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            raise PrintfulAPIError(
                f"API request failed with status {response.status_code}",
                status_code=response.status_code
            )
        
        # v2 API errors are returned as either RFC 9457 ({"detail"/"title"})
        # or Printful's nested form {"data": <msg>, "error": {"message": ...}}.
        # Extract whichever carries the real message so 4xx responses surface
        # their actual text instead of a generic fallback.
        if version == "v2":
            nested = error_data.get("error") or {}
            data_field = error_data.get("data")
            error_msg = (
                error_data.get("detail")
                or error_data.get("title")
                or nested.get("message")
                or (data_field if isinstance(data_field, str) else None)
                or f"API request failed with status {response.status_code}"
            )
            raise PrintfulAPIError(
                error_msg,
                status_code=response.status_code,
                detail=error_data
            )
        # v1 API format
        else:
            error_msg = error_data.get("error", {}).get("message", "Unknown error")
            raise PrintfulAPIError(
                error_msg,
                status_code=response.status_code,
                detail=error_data
            )
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    # Convenience methods for common operations
    async def get(self, endpoint: str, version: str = "v2", **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", endpoint, version=version, **kwargs)
    
    async def post(self, endpoint: str, json_data: Dict[str, Any], version: str = "v2", **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", endpoint, version=version, json_data=json_data, **kwargs)
    
    async def patch(self, endpoint: str, json_data: Dict[str, Any], version: str = "v2", **kwargs) -> Dict[str, Any]:
        """Make a PATCH request."""
        return await self.request("PATCH", endpoint, version=version, json_data=json_data, **kwargs)
    
    async def delete(self, endpoint: str, version: str = "v2", **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", endpoint, version=version, **kwargs)
