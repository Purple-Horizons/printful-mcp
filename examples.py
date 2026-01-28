"""
Example usage of Printful MCP Server tools.

This file demonstrates how to use the various tools programmatically.
When used with Cursor/Claude Desktop, you'd simply ask in natural language.
"""

# Example 1: Browse the catalog
"""
Natural language: "Show me t-shirts with DTG printing in the catalog"

Tool call:
printful_list_catalog_products(
    types="T-SHIRT",
    techniques="dtg",
    limit=5,
    format="markdown"
)
"""

# Example 2: Get product details
"""
Natural language: "Get details for product 71"

Tool call:
printful_get_product(
    product_id=71,
    format="markdown"
)
"""

# Example 3: Get variants for a product
"""
Natural language: "What sizes and colors are available for product 71?"

Tool call:
printful_get_product_variants(
    product_id=71,
    limit=20,
    format="markdown"
)
"""

# Example 4: Check pricing
"""
Natural language: "What's the price for variant 4011 in USD?"

Tool call:
printful_get_variant_prices(
    variant_id=4011,
    currency="USD",
    format="markdown"
)
"""

# Example 5: Calculate shipping
"""
Natural language: "Calculate shipping to Los Angeles for a t-shirt order"

Tool call:
printful_calculate_shipping(
    recipient_country_code="US",
    recipient_state_code="CA",
    recipient_city="Los Angeles",
    recipient_zip="90001",
    items_json='[{"catalog_variant_id": 4011, "quantity": 1, "source": "catalog", "placements": [{"placement": "front", "technique": "dtg", "layers": [{"type": "file", "url": "https://example.com/design.png"}]}]}]',
    format="markdown"
)
"""

# Example 6: Create an order
"""
Natural language: "Create an order for John Doe at 123 Main St, Los Angeles, CA 90001"

Tool call:
printful_create_order(
    recipient_name="John Doe",
    recipient_address1="123 Main St",
    recipient_city="Los Angeles",
    recipient_state_code="CA",
    recipient_country_code="US",
    recipient_zip="90001",
    recipient_email="john@example.com",
    external_id="my-order-123",
    format="markdown"
)
"""

# Example 7: Generate mockups
"""
Natural language: "Generate a mockup for product 71, variant 4011, style 1115, with my design"

Tool call:
printful_create_mockup_task(
    product_id=71,
    variant_ids="4011",
    mockup_style_ids="1115",
    design_url="https://example.com/design.png",
    placement="front",
    technique="dtg",
    format="jpg"
)

# Then check status:
printful_get_mockup_task(
    task_id="<returned-task-id>",
    format="markdown"
)
"""

# Example 8: Complete order workflow
"""
Natural language: "Create and confirm an order for a white t-shirt with my logo"

Workflow:
1. Browse catalog → "Show me white t-shirts"
2. Get variants → "What sizes are available for product X?"
3. Calculate shipping → "Calculate shipping to <address>"
4. Create order → "Create an order to <recipient>"
5. Add items → (Include items in create_order or add separately)
6. Confirm order → "Confirm order <order-id>"
"""

# Example 9: Check order status
"""
Natural language: "What's the status of order 12345?"

Tool call:
printful_get_order(
    order_id="12345",
    format="markdown"
)

# Or with external ID:
printful_get_order(
    order_id="@my-order-123",
    format="markdown"
)
"""

# Example 10: List stores
"""
Natural language: "Show me my Printful stores"

Tool call:
printful_list_stores(format="markdown")
"""

# Example 11: Get store statistics
"""
Natural language: "Show me sales stats for store 12345 in January 2024"

Tool call:
printful_get_store_stats(
    store_id=12345,
    date_from="2024-01-01",
    date_to="2024-01-31",
    report_types="sales_and_costs,profit,total_paid_orders",
    format="markdown"
)
"""

# Example 12: Upload a design file
"""
Natural language: "Upload my design file from URL"

Tool call:
printful_add_file(
    url="https://example.com/my-design.png",
    filename="my-design.png",
    visible=True,
    format="markdown"
)
"""

# Example 13: Check stock availability
"""
Natural language: "Is product 71 in stock?"

Tool call:
printful_get_product_availability(
    product_id=71,
    format="markdown"
)
"""

# Example 14: List sync products (v1 fallback)
"""
Natural language: "Show me my sync products"

Tool call:
printful_list_sync_products(
    limit=20,
    format="markdown"
)
"""

print("See comments above for example usage patterns!")
print("\nWhen using with Cursor/Claude Desktop:")
print("- Just ask in natural language")
print("- The AI will automatically call the right tools")
print("- No need to know exact parameter names")
