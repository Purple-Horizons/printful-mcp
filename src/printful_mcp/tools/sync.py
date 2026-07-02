"""v1 API fallback tools for features not yet available in v2."""

import json
from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional
from ..client import PrintfulClient, PrintfulAPIError


# v1 Sync Product Models
class ListSyncProductsInput(BaseModel):
    """Input for listing sync products (v2 /v2/sync-products)."""
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Number of results per page")
    offset: Optional[int] = Field(default=0, ge=0, description="Number of results to skip")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetSyncProductInput(BaseModel):
    """Input for getting sync product (v1 only)."""
    sync_product_id: int = Field(..., description="Sync product ID")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


async def list_sync_products(client: PrintfulClient, params: ListSyncProductsInput) -> str:
    """
    List sync products using the v2 API (/v2/sync-products).

    Sync products are pre-configured product templates with saved designs
    that can be quickly added to orders. Unlike the v1 /store/products
    endpoint, the v2 endpoint works for external-platform stores (Shopify,
    Etsy, etc.), not just Manual Order / API stores.
    """
    try:
        query_params = {
            "limit": params.limit,
            "offset": params.offset,
        }

        # Use v2 API. The client's v2 base URL already includes "/v2", so the
        # endpoint is "/sync-products". The response is
        # {"data": [...], "paging": {...}}, returned verbatim (no "result" unwrapping).
        data = await client.get("/sync-products", version="v2", params=query_params)

        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            products = data.get("data", []) if isinstance(data, dict) else []
            total = (data.get("paging") or {}).get("total") if isinstance(data, dict) else None

            count_label = f"{len(products)} shown"
            if total is not None:
                count_label = f"{len(products)} of {total}"

            lines = [
                f"# Sync Products ({count_label})",
                f"",
            ]

            for product in products:
                lines.append(f"## {product.get('name', 'Unnamed')}")
                lines.append(f"- **Sync Product ID:** {product.get('id', 'N/A')}")
                lines.append(f"- **External ID:** {product.get('external_id', 'N/A')}")
                if product.get("is_ignored"):
                    lines.append(f"- **Status:** Ignored")
                if product.get("thumbnail_url"):
                    lines.append(f"- **Thumbnail:** {product['thumbnail_url']}")
                lines.append(f"")

            return "\n".join(lines)

    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_sync_product(client: PrintfulClient, params: GetSyncProductInput) -> str:
    """
    Get sync product details using the v2 API (/v2/sync-products/{id}).

    Returns full details of a sync product including its variants. Unlike the
    v1 /store/products/{id} endpoint, the v2 endpoint works for external-platform
    stores (Shopify, Etsy, etc.). In v2 the product and its variants are separate
    resources, so this fetches both /sync-products/{id} and its /sync-variants.
    """
    try:
        # Use v2 API. Base URL already includes "/v2". The product endpoint
        # returns {"data": {product}, "extra": []}; variants are a sub-resource
        # returning {"data": [variants], "paging": {...}}.
        product_resp = await client.get(
            f"/sync-products/{params.sync_product_id}", version="v2"
        )
        variants_resp = await client.get(
            f"/sync-products/{params.sync_product_id}/sync-variants", version="v2"
        )

        if params.format == "json":
            return json.dumps(
                {"product": product_resp, "variants": variants_resp}, indent=2
            )
        else:
            product = product_resp.get("data", {}) if isinstance(product_resp, dict) else {}
            variants = variants_resp.get("data", []) if isinstance(variants_resp, dict) else []

            lines = [
                f"# {product.get('name', 'Sync Product')}",
                f"",
                f"**Sync Product ID:** {product.get('id', 'N/A')}",
                f"**External ID:** {product.get('external_id', 'N/A')}",
                f"**Thumbnail:** {product.get('thumbnail_url', 'N/A')}",
            ]
            if product.get("is_ignored"):
                lines.append(f"**Status:** Ignored")
            lines.append(f"")

            if variants:
                lines.append(f"## Sync Variants ({len(variants)})")
                for variant in variants:
                    lines.extend([
                        f"### Variant {variant.get('id', 'N/A')}",
                        f"- **Name:** {variant.get('name', 'N/A')}",
                        f"- **External ID:** {variant.get('external_id', 'N/A')}",
                        f"- **Catalog Variant ID:** {variant.get('catalog_variant_id', 'N/A')}",
                        f"- **Retail Price:** {variant.get('retail_price', 'N/A')} {variant.get('currency', '')}",
                        f"",
                    ])

            return "\n".join(lines)

    except PrintfulAPIError as e:
        return f"Error: {e.message}"
