"""v1 API fallback tools for features not yet available in v2."""

import json
from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional
from ..client import PrintfulClient, PrintfulAPIError


# v1 Sync Product Models
class ListSyncProductsInput(BaseModel):
    """Input for listing sync products (v1 only)."""
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Number of results per page")
    offset: Optional[int] = Field(default=0, ge=0, description="Number of results to skip")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetSyncProductInput(BaseModel):
    """Input for getting sync product (v1 only)."""
    sync_product_id: int = Field(..., description="Sync product ID")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


async def list_sync_products(client: PrintfulClient, params: ListSyncProductsInput) -> str:
    """
    List sync products using v1 API (not available in v2 yet).
    
    Sync products are pre-configured product templates with saved designs
    that can be quickly added to orders. This uses the v1 API as sync
    products are not yet available in v2.
    """
    try:
        query_params = {
            "limit": params.limit,
            "offset": params.offset,
        }
        
        # Use v1 API
        data = await client.get("/store/products", version="v1", params=query_params)
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            products = data if isinstance(data, list) else []
            
            lines = [
                f"# Sync Products ({len(products)} shown)",
                f"",
                f"**Note:** Using v1 API (sync products not yet in v2)",
                f"",
            ]
            
            for product in products:
                lines.extend([
                    f"## {product.get('name', 'Unnamed')}",
                    f"- **Sync Product ID:** {product['id']}",
                    f"- **Sync Variants:** {len(product.get('sync_variants', []))}",
                    f"- **External ID:** {product.get('external_id', 'N/A')}",
                    f"",
                ])
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_sync_product(client: PrintfulClient, params: GetSyncProductInput) -> str:
    """
    Get sync product details using v1 API (not available in v2 yet).
    
    Returns full details of a sync product including variants and designs.
    This uses the v1 API as sync products are not yet available in v2.
    """
    try:
        # Use v1 API
        data = await client.get(f"/store/products/{params.sync_product_id}", version="v1")
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            product = data.get('sync_product', {})
            variants = data.get('sync_variants', [])
            
            lines = [
                f"# {product.get('name', 'Sync Product')}",
                f"",
                f"**Sync Product ID:** {product['id']}",
                f"**External ID:** {product.get('external_id', 'N/A')}",
                f"**Thumbnail:** {product.get('thumbnail_url', 'N/A')}",
                f"",
                f"**Note:** Using v1 API (sync products not yet in v2)",
                f"",
            ]
            
            if variants:
                lines.append(f"## Sync Variants ({len(variants)})")
                for variant in variants:
                    lines.extend([
                        f"### Variant {variant['id']}",
                        f"- **Name:** {variant.get('name', 'N/A')}",
                        f"- **External ID:** {variant.get('external_id', 'N/A')}",
                        f"- **Variant ID:** {variant.get('variant_id', 'N/A')}",
                        f"- **Retail Price:** {variant.get('retail_price', 'N/A')} {variant.get('currency', '')}",
                        f"",
                    ])
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
