---
name: printful-mcp
description: Automate Printful print-on-demand operations through AI. Use when the user asks about Printful, print-on-demand, POD, product catalogs, orders, mockups, shipping rates, or store management. Helps browse products, create orders, generate mockups, and manage fulfillment.
---

# Printful MCP Automation

Expert guidance for automating Printful print-on-demand workflows using the Printful MCP server's 17 tools.

## Quick Reference

**When to use this skill:**
- Browsing Printful's product catalog
- Creating and managing orders
- Generating product mockups
- Calculating shipping rates
- Managing store operations
- Checking product availability
- Uploading design files

## Available Tool Categories

| Category | Tools | Common Use Cases |
|----------|-------|------------------|
| 🛍️ **Catalog** (5) | Browse, search, pricing | "Show me all t-shirts under $15" |
| 📦 **Orders** (4) | Create, manage, fulfill | "Create order for John in LA" |
| 🚚 **Shipping** (2) | Rates, countries | "How much to ship to UK?" |
| 🖼️ **Mockups** (2) | Generate, check status | "Create mockup with my design" |
| 📁 **Files** (2) | Upload, retrieve | "Upload my logo file" |
| 🏪 **Stores** (2) | List, statistics | "Show my store sales" |
| 🔄 **Sync** (2) | Legacy products | "List my synced products" |

## Common Workflows

### 1. Product Discovery Workflow

**User asks:** "Find me a product to print my design on"

**Steps:**
1. **Browse catalog** by category or technique
2. **Check availability** for specific variants
3. **Get pricing** in user's currency
4. **Show variants** (sizes/colors)

**Example prompts to use:**
```
"Show me all hoodies available for DTG printing"
"What sizes does product 71 come in?"
"How much is variant 4011 in USD?"
"Is this variant in stock?"
```

### 2. Order Creation Workflow

**User asks:** "Create an order for my customer"

**Steps:**
1. **Create draft order** with recipient details
2. **Add items** (if not done in creation)
3. **Calculate shipping** (optional, for transparency)
4. **Confirm order** to start fulfillment

**Example prompts:**
```
"Create draft order for John Doe, 123 Main St, Los Angeles CA 90001"
"Calculate shipping to that address"
"Confirm order ID 12345"
```

**⚠️ Important:** Orders are created as DRAFTS. Must be explicitly confirmed to start production.

### 3. Mockup Generation Workflow

**User asks:** "Show me how my design looks on a product"

**Steps:**
1. **Create mockup task** with design URL and product details
2. **Wait 10-30 seconds** (mockup generation takes time)
3. **Check task status** to get mockup URLs
4. **Display mockups** to user

**Example prompts:**
```
"Generate mockup for product 71 with my design at https://example.com/design.png"
"Check status of mockup task 597350033"
```

**⚠️ Note:** Mockup generation is async. Always check status after creating task.

### 4. Store Analysis Workflow

**User asks:** "How's my store doing?"

**Steps:**
1. **List stores** (if multiple)
2. **Get statistics** for target store
3. **Present metrics** clearly

**Example prompts:**
```
"Show all my Printful stores"
"What are the sales stats for store 14690720?"
```

## Best Practices

### ✅ Do This

**1. Use natural language queries**
```
✅ "Show me all t-shirts under $15"
✅ "Create order for John at 123 Main St, LA"
✅ "How much to ship to UK?"
```

**2. Check availability before ordering**
```
✅ First: "Is variant 4011 in stock?"
✅ Then: "Create order with variant 4011"
```

**3. Wait for mockup generation**
```
✅ Create task → Wait 15-30s → Check status
❌ Create task → Immediately check status (will be pending)
```

**4. Use external IDs for order tracking**
```
✅ Create order with external_id="my-shop-order-789"
✅ Reference as @my-shop-order-789 later
```

**5. Request markdown format for readability**
```
✅ Most tools support format="markdown" (default)
✅ Use format="json" only for programmatic processing
```

### ❌ Avoid This

**1. Don't guess product/variant IDs**
```
❌ "Order variant 9999999" (probably doesn't exist)
✅ "Search for hoodies first, then order"
```

**2. Don't skip draft order confirmation**
```
❌ Creating order and assuming it's sent to production
✅ Create draft → Review → Explicitly confirm
```

**3. Don't exceed rate limits**
```
❌ Making 100+ requests in quick succession
✅ Batch operations, space out requests
Rate limit: 120 requests per 60 seconds
```

**4. Don't use store-specific features on account tokens**
```
❌ Using account-level token without specifying PRINTFUL_STORE_ID
✅ Either use single-store token OR set PRINTFUL_STORE_ID env var
```

## Tool Reference

### 🛍️ Catalog Tools

**printful_list_catalog_products**
- Browse 300+ products with filters
- Filter by: type, category, technique, brand
- Returns: Product list with IDs, names, images, prices

**printful_get_product**
- Detailed product information
- Includes: Placements, techniques, available files
- Use: When user wants deep product details

**printful_get_product_variants**
- All size/color combinations
- Returns: Variant IDs, names, dimensions
- Use: "What sizes are available?"

**printful_get_variant_prices**
- Pricing by currency
- Supports: USD, EUR, GBP, CAD, etc.
- Use: "How much in euros?"

**printful_get_product_availability**
- Real-time stock status
- Returns: Available regions, stock levels
- Use: Before creating orders

### 📦 Order Tools

**printful_create_order**
- Create draft order with recipient
- Required: Name, address, city, state, country, zip
- Optional: Phone, email, external_id
- Returns: Order ID (save this!)

**printful_get_order**
- View order details and status
- Use order ID or @external_id
- Returns: Full order with items, status, tracking

**printful_confirm_order**
- Start production/fulfillment
- ⚠️ **Cannot be undone**
- ⚠️ **Charges your account**
- Use: After reviewing draft order

**printful_list_orders**
- List all orders with filters
- Filter by: Status, external_id
- Use: "Show my recent orders"

### 🚚 Shipping Tools

**printful_calculate_shipping**
- Get shipping rates and delivery times
- Required: Recipient address, items
- Returns: Available carriers and costs

**printful_list_countries**
- Supported countries and states
- Use: Validate addresses
- Returns: Country codes, state codes

### 🖼️ Mockup Tools

**printful_create_mockup_task**
- Generate product mockup images
- Required: Product ID, variant IDs, design URL
- Optional: Placement, technique, format
- Returns: Task ID (not the mockups yet!)

**printful_get_mockup_task**
- Check generation status
- Returns: Status + mockup URLs when ready
- Use: 15-30 seconds after creating task

### 📁 File Tools

**printful_add_file**
- Upload design file to library
- Accepts: URL or base64 data
- Returns: File ID for later use

**printful_get_file**
- Get file information
- Returns: URL, status, dimensions
- Use: Check upload status

### 🏪 Store Tools

**printful_list_stores**
- List all your stores
- Use: Multi-store accounts
- Returns: Store IDs, names, types

**printful_get_store_stats**
- Sales and profit metrics
- Optional: Date range, currency
- Returns: Revenue, costs, profit

### 🔄 Sync Product Tools (v1 API)

**printful_list_sync_products**
- List products synced to store
- ⚠️ Only works with Printful stores (not Etsy, Shopify, etc.)
- Use: "Show my store products"

**printful_get_sync_product**
- Detailed sync product info
- Returns: Variants, sync status
- Use: "Details on sync product 123"

## Troubleshooting

### "PRINTFUL_API_KEY environment variable is required"
**Solution:** API key not configured in MCP settings
- Check `~/.cursor/mcp.json` or Claude Desktop config
- Ensure `PRINTFUL_API_KEY` is set in `env` section

### "Rate limit exceeded"
**Solution:** Wait 60 seconds, then retry
- Default limit: 120 requests/minute
- Implement pauses between bulk operations

### "Resource not found"
**Solution:** ID doesn't exist or wrong format
- For orders: Use actual order ID or @external_id format
- For products: Browse catalog first to get valid IDs

### "This API endpoint applies only to Printful stores"
**Solution:** Using sync product tools with third-party store
- Sync products only work with native Printful stores
- Not compatible with Etsy, Shopify, WooCommerce stores

### Mockup stuck on "pending"
**Solution:** Wait longer or check for errors
- Normal wait time: 10-30 seconds
- After 2 minutes: Task likely failed, check error message

## Common User Questions

**Q: "Can I browse your catalog?"**
→ Use `printful_list_catalog_products` with filters

**Q: "How much does shipping cost?"**
→ Use `printful_calculate_shipping` with address and items

**Q: "Create an order for my customer"**
→ Use `printful_create_order` → Review → `printful_confirm_order`

**Q: "Show me how my design looks"**
→ Use `printful_create_mockup_task` → Wait → `printful_get_mockup_task`

**Q: "What are my store stats?"**
→ Use `printful_list_stores` then `printful_get_store_stats`

**Q: "Is this product in stock?"**
→ Use `printful_get_product_availability`

## Output Format Guidelines

When presenting results to users:

**For product lists:**
```markdown
Found 5 t-shirts:
1. Bella Canvas 3001 - $5.95 (DTG)
2. Gildan 5000 - $4.50 (DTG)
...
```

**For orders:**
```markdown
Order #12345 created (DRAFT)
- Recipient: John Doe
- Address: 123 Main St, Los Angeles CA 90001
- Status: Draft (not yet sent to production)

Next step: Confirm order to start fulfillment
```

**For shipping rates:**
```markdown
Shipping to UK:
- Standard: $8.50 (7-14 business days)
- Express: $15.00 (3-5 business days)
```

**For errors:**
```markdown
❌ Error: Rate limit exceeded
⏱️ Wait 45 seconds and try again
```

## Advanced Patterns

### Bulk Product Lookup
```
For each product in user's list:
1. Get product details
2. Check availability
3. Get pricing
4. Present summary table
```

### Order Validation Flow
```
1. Calculate shipping first
2. Show customer total cost
3. Get user confirmation
4. Create order
5. Confirm order
```

### Multi-Store Management
```
1. List all stores
2. Get stats for each
3. Compare performance
4. Present consolidated view
```

## API Version Notes

- **Primary:** API v2 (beta, but production-ready)
- **Fallback:** API v1 for sync products
- **Auto-switching:** Server handles version selection
- **Future-proof:** v2 will become standard

## Quick Tips

💡 **Always use markdown format** for user-facing results
💡 **Wait 15-30 seconds** after creating mockup tasks
💡 **Confirm orders explicitly** - drafts don't auto-confirm
💡 **Use external IDs** for easier order tracking
💡 **Check availability** before creating orders
💡 **Batch operations** to avoid rate limits
💡 **Validate addresses** with `printful_list_countries` first

## Additional Resources

For detailed documentation:
- [README.md](../../../README.md) - Full setup and usage guide
- [QUICKSTART.md](../../../QUICKSTART.md) - 3-minute setup
- [API_TOKEN_SETUP.md](../../../API_TOKEN_SETUP.md) - API key configuration
- [TESTING.md](../../../TESTING.md) - Testing strategies

For support:
- GitHub Issues: Report bugs or request features
- Printful API Docs: https://developers.printful.com/docs/v2-beta/
- Purple Horizons: https://purplehorizons.io
