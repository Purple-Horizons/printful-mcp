"""Catalog tools for Printful MCP server."""

import json
from typing import Dict, Any
from ..client import PrintfulClient, PrintfulAPIError
from ..models.inputs import (
    ListCatalogProductsInput,
    GetProductInput,
    GetProductVariantsInput,
    GetVariantPricesInput,
    GetProductAvailabilityInput,
)


def format_product_markdown(product: Dict[str, Any]) -> str:
    """Format product data as markdown."""
    lines = [
        f"# {product['name']}",
        f"",
        f"**ID:** {product['id']}",
        f"**Type:** {product['type']}",
        f"**Brand:** {product.get('brand', 'N/A')}",
        f"**Variants:** {product['variant_count']}",
        f"**Status:** {'Discontinued' if product['is_discontinued'] else 'Available'}",
        f"",
    ]
    
    if product.get('description'):
        lines.extend([
            "## Description",
            product['description'],
            "",
        ])
    
    if product.get('techniques'):
        lines.append("## Available Techniques")
        for tech in product['techniques']:
            default = " (default)" if tech.get('is_default') else ""
            lines.append(f"- **{tech['display_name']}** ({tech['key']}){default}")
        lines.append("")
    
    if product.get('placements'):
        lines.append(f"## Placements ({len(product['placements'])} available)")
        for placement in product['placements'][:5]:  # Show first 5
            lines.append(f"- {placement['placement']} - {placement['technique']}")
        if len(product['placements']) > 5:
            lines.append(f"  _(and {len(product['placements']) - 5} more)_")
        lines.append("")
    
    return "\n".join(lines)


def format_products_list_markdown(data: Dict[str, Any]) -> str:
    """Format products list as markdown."""
    products = data.get('data', [])
    paging = data.get('paging', {})
    
    lines = [
        f"# Catalog Products ({paging.get('total', 0)} total)",
        f"",
        f"Showing {len(products)} products (offset: {paging.get('offset', 0)}, limit: {paging.get('limit', 20)})",
        f"",
    ]
    
    for product in products:
        lines.extend([
            f"## {product['name']}",
            f"- **ID:** {product['id']}",
            f"- **Type:** {product['type']}",
            f"- **Variants:** {product['variant_count']}",
            f"- **Techniques:** {', '.join(t['key'] for t in product.get('techniques', []))}",
            f"",
        ])
    
    return "\n".join(lines)


async def list_catalog_products(client: PrintfulClient, params: ListCatalogProductsInput) -> str:
    """
    List catalog products with optional filters.
    
    Browse Printful's product catalog with filtering by category, color, technique, etc.
    Returns product IDs, names, types, and available variants.
    """
    try:
        query_params = {
            "limit": params.limit,
            "offset": params.offset,
        }
        
        if params.category_ids:
            query_params["category_ids"] = params.category_ids
        if params.colors:
            query_params["colors"] = params.colors
        if params.techniques:
            query_params["techniques"] = params.techniques
        if params.types:
            query_params["types"] = params.types
        
        data = await client.get("/catalog-products", params=query_params)
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            return format_products_list_markdown(data)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_product(client: PrintfulClient, params: GetProductInput) -> str:
    """
    Get detailed information about a specific catalog product.
    
    Returns full product details including placements, techniques, design options,
    available sizes, colors, and product options.
    """
    try:
        data = await client.get(f"/catalog-products/{params.product_id}")
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            product = data.get('data', {})
            return format_product_markdown(product)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_product_variants(client: PrintfulClient, params: GetProductVariantsInput) -> str:
    """
    Get all variants (size/color combinations) for a catalog product.
    
    Returns variant IDs, names, sizes, colors, and images needed for ordering.
    """
    try:
        query_params = {
            "limit": params.limit,
            "offset": params.offset,
        }
        
        data = await client.get(
            f"/catalog-products/{params.product_id}/catalog-variants",
            params=query_params
        )
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            variants = data.get('data', [])
            paging = data.get('paging', {})
            
            lines = [
                f"# Variants for Product {params.product_id}",
                f"",
                f"Total variants: {paging.get('total', 0)}",
                f"Showing {len(variants)} variants",
                f"",
            ]
            
            for variant in variants:
                lines.extend([
                    f"## {variant['name']}",
                    f"- **Variant ID:** {variant['id']}",
                    f"- **Size:** {variant['size']}",
                    f"- **Color:** {variant['color']} ({variant['color_code']})",
                    f"",
                ])
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_variant_prices(client: PrintfulClient, params: GetVariantPricesInput) -> str:
    """
    Get pricing information for a specific catalog variant.
    
    Returns prices for different techniques, placements, and quantity discounts.
    """
    try:
        query_params = {}
        if params.currency:
            query_params["currency"] = params.currency
        
        data = await client.get(
            f"/catalog-variants/{params.variant_id}/prices",
            params=query_params
        )
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            price_data = data.get('data', {})
            currency = price_data.get('currency', 'USD')
            
            lines = [
                f"# Pricing for Variant {params.variant_id}",
                f"",
                f"**Currency:** {currency}",
                f"",
            ]
            
            # Variant base prices
            if price_data.get('variant', {}).get('techniques'):
                lines.append("## Base Prices by Technique")
                for tech in price_data['variant']['techniques']:
                    lines.append(
                        f"- **{tech['technique_display_name']}:** "
                        f"{tech['price']} {currency}"
                    )
                lines.append("")
            
            # Placement prices
            if price_data.get('product', {}).get('placements'):
                lines.append("## Additional Placement Prices")
                for placement in price_data['product']['placements']:
                    lines.append(
                        f"- **{placement['title']}:** "
                        f"{placement['price']} {currency}"
                    )
                lines.append("")
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_product_availability(client: PrintfulClient, params: GetProductAvailabilityInput) -> str:
    """
    Check stock availability for a catalog product.
    
    Returns availability status for each variant and technique.
    """
    try:
        query_params = {}
        if params.techniques:
            query_params["techniques"] = params.techniques
        
        data = await client.get(
            f"/catalog-products/{params.product_id}/availability",
            params=query_params
        )
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            variants = data.get('data', [])
            
            lines = [
                f"# Availability for Product {params.product_id}",
                f"",
            ]
            
            for variant in variants:
                lines.append(f"## Variant {variant['catalog_variant_id']}")
                for tech in variant.get('techniques', []):
                    lines.append(f"### {tech['technique']}")
                    for region in tech.get('selling_regions', []):
                        status = region['availability']
                        lines.append(f"- **{region['name']}:** {status}")
                lines.append("")
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
