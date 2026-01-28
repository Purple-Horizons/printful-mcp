"""Printful MCP Server - Main server implementation."""

import asyncio
import atexit
import os
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from .client import PrintfulClient
from .models.inputs import (
    ListCatalogProductsInput,
    GetProductInput,
    GetProductVariantsInput,
    GetVariantPricesInput,
    GetProductAvailabilityInput,
    CreateOrderInput,
    GetOrderInput,
    ConfirmOrderInput,
    ListOrdersInput,
    CalculateShippingInput,
    CreateMockupTaskInput,
    GetMockupTaskInput,
    AddFileInput,
    GetFileInput,
    ListStoresInput,
    GetStoreStatsInput,
)
from .tools import catalog, orders, shipping, mockups, files, stores, sync
from .tools.sync import ListSyncProductsInput, GetSyncProductInput

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP("printful_mcp")

# Global client instance (lazily initialized)
_client: PrintfulClient = None


def _cleanup_client():
    """Close the client on exit."""
    global _client
    if _client is not None:
        try:
            asyncio.get_event_loop().run_until_complete(_client.close())
        except Exception:
            pass  # Best effort cleanup


def get_client() -> PrintfulClient:
    """Get or create the PrintfulClient instance."""
    global _client
    if _client is None:
        _client = PrintfulClient()
        atexit.register(_cleanup_client)
    return _client


# ========== CATALOG TOOLS ==========

@mcp.tool(
    name="printful_list_catalog_products",
    annotations={
        "title": "List Printful Catalog Products",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_list_catalog_products(params: ListCatalogProductsInput) -> str:
    """
    Browse Printful's product catalog with optional filters.
    
    Returns a list of available products including t-shirts, mugs, posters, etc.
    Use filters to narrow down by category, color, technique, or product type.
    """
    return await catalog.list_catalog_products(get_client(), params)


@mcp.tool(
    name="printful_get_product",
    annotations={
        "title": "Get Printful Product Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_product(params: GetProductInput) -> str:
    """
    Get detailed information about a specific catalog product.
    
    Returns placements (where designs can be printed), techniques (DTG, embroidery, etc.),
    available sizes/colors, and design requirements.
    """
    return await catalog.get_product(get_client(), params)


@mcp.tool(
    name="printful_get_product_variants",
    annotations={
        "title": "Get Product Variants",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_product_variants(params: GetProductVariantsInput) -> str:
    """
    Get all variants (size/color combinations) for a product.
    
    Each variant has a unique ID needed for ordering. Returns variant IDs,
    names, sizes, colors, and preview images.
    """
    return await catalog.get_product_variants(get_client(), params)


@mcp.tool(
    name="printful_get_variant_prices",
    annotations={
        "title": "Get Variant Pricing",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_variant_prices(params: GetVariantPricesInput) -> str:
    """
    Get pricing information for a specific variant.
    
    Returns base prices by technique, placement costs, and quantity discounts.
    Helps calculate total order costs before ordering.
    """
    return await catalog.get_variant_prices(get_client(), params)


@mcp.tool(
    name="printful_get_product_availability",
    annotations={
        "title": "Check Product Stock Availability",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_product_availability(params: GetProductAvailabilityInput) -> str:
    """
    Check stock availability for a product's variants.
    
    Returns in-stock/out-of-stock status for each variant and technique
    by selling region. Critical for displaying product availability.
    """
    return await catalog.get_product_availability(get_client(), params)


# ========== ORDER TOOLS ==========

@mcp.tool(
    name="printful_create_order",
    annotations={
        "title": "Create Printful Order",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def printful_create_order(params: CreateOrderInput) -> str:
    """
    Create a new order in draft status.
    
    Creates an empty order with recipient info. Add items separately, then
    confirm to start fulfillment. Draft orders are not charged.
    """
    return await orders.create_order(get_client(), params)


@mcp.tool(
    name="printful_get_order",
    annotations={
        "title": "Get Order Details",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_order(params: GetOrderInput) -> str:
    """
    Get details of a specific order.
    
    Returns order status, recipient, costs, items, and shipment info.
    Use order ID or external ID (prefix with @).
    """
    return await orders.get_order(get_client(), params)


@mcp.tool(
    name="printful_confirm_order",
    annotations={
        "title": "Confirm Order for Fulfillment",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def printful_confirm_order(params: ConfirmOrderInput) -> str:
    """
    Confirm an order to start production and fulfillment.
    
    Moves order from draft to pending status. Order will be charged and
    sent to production. Cannot be undone easily.
    """
    return await orders.confirm_order(get_client(), params)


@mcp.tool(
    name="printful_list_orders",
    annotations={
        "title": "List All Orders",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_list_orders(params: ListOrdersInput) -> str:
    """
    List all orders from the store.
    
    Returns paginated list of orders with status, costs, and item counts.
    """
    return await orders.list_orders(get_client(), params)


# ========== SHIPPING TOOLS ==========

@mcp.tool(
    name="printful_calculate_shipping",
    annotations={
        "title": "Calculate Shipping Rates",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_calculate_shipping(params: CalculateShippingInput) -> str:
    """
    Calculate shipping rates for an order.
    
    Returns available shipping methods, costs, and estimated delivery times
    based on recipient location and order items.
    """
    return await shipping.calculate_shipping_rates(get_client(), params)


@mcp.tool(
    name="printful_list_countries",
    annotations={
        "title": "List Available Countries",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def printful_list_countries() -> str:
    """
    List all countries where Printful ships.
    
    Returns country codes and state codes needed for creating orders.
    Essential for address validation.
    """
    return await shipping.list_countries(get_client())


# ========== MOCKUP TOOLS ==========

@mcp.tool(
    name="printful_create_mockup_task",
    annotations={
        "title": "Create Mockup Generation Task",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
)
async def printful_create_mockup_task(params: CreateMockupTaskInput) -> str:
    """
    Generate product mockup images.
    
    Creates an async task to generate mockup images showing your design
    on the product. Returns task ID to check status and get URLs.
    """
    return await mockups.create_mockup_task(get_client(), params)


@mcp.tool(
    name="printful_get_mockup_task",
    annotations={
        "title": "Get Mockup Task Status",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_mockup_task(params: GetMockupTaskInput) -> str:
    """
    Check mockup generation status and get results.
    
    Returns task status (pending/completed/failed) and mockup image URLs
    if completed. Typically takes 10-30 seconds to generate.
    """
    return await mockups.get_mockup_task(get_client(), params)


# ========== FILE TOOLS ==========

@mcp.tool(
    name="printful_add_file",
    annotations={
        "title": "Add File to Library",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_add_file(params: AddFileInput) -> str:
    """
    Add a design file to the Printful file library.
    
    Uploads file from URL for reuse across orders. Files are processed
    asynchronously. Returns file ID for use in orders.
    """
    return await files.add_file(get_client(), params)


@mcp.tool(
    name="printful_get_file",
    annotations={
        "title": "Get File Information",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_file(params: GetFileInput) -> str:
    """
    Get information about a file in the library.
    
    Returns file status, dimensions, DPI, and URLs. Check processing
    status before using in orders.
    """
    return await files.get_file(get_client(), params)


# ========== STORE TOOLS ==========

@mcp.tool(
    name="printful_list_stores",
    annotations={
        "title": "List Stores",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def printful_list_stores(params: ListStoresInput) -> str:
    """
    List all stores available to your API token.
    
    Returns store IDs and names. Needed for multi-store accounts.
    """
    return await stores.list_stores(get_client(), params)


@mcp.tool(
    name="printful_get_store_stats",
    annotations={
        "title": "Get Store Statistics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_store_stats(params: GetStoreStatsInput) -> str:
    """
    Get store statistics for a date range.
    
    Returns sales, costs, profit, order counts, and fulfillment metrics.
    Date range cannot exceed 6 months.
    """
    return await stores.get_store_statistics(get_client(), params)


# ========== V1 FALLBACK TOOLS ==========

@mcp.tool(
    name="printful_list_sync_products",
    annotations={
        "title": "List Sync Products (v1)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_list_sync_products(params: ListSyncProductsInput) -> str:
    """
    List sync products using v1 API (not available in v2 yet).
    
    Sync products are pre-configured templates with saved designs.
    Currently only available via v1 API.
    """
    return await sync.list_sync_products(get_client(), params)


@mcp.tool(
    name="printful_get_sync_product",
    annotations={
        "title": "Get Sync Product Details (v1)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def printful_get_sync_product(params: GetSyncProductInput) -> str:
    """
    Get sync product details using v1 API (not available in v2 yet).
    
    Returns full sync product info including variants and designs.
    Currently only available via v1 API.
    """
    return await sync.get_sync_product(get_client(), params)


def main():
    """Entry point for the MCP server (stdio only, for backwards compatibility).
    
    For full CLI with transport options, use: python -m printful_mcp --help
    """
    # Check for API key
    if not os.getenv("PRINTFUL_API_KEY"):
        print("Error: PRINTFUL_API_KEY environment variable is required", file=sys.stderr)
        print("Get your API key from: https://www.printful.com/dashboard/api", file=sys.stderr)
        sys.exit(1)
    
    # Run the server with stdio transport (default for Cursor/Claude Desktop)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
