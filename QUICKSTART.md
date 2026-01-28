# Quick Start Guide

## Setup in 3 Steps

### 1. Get Your Printful API Key

1. Go to https://www.printful.com/dashboard/api
2. Create a new API token with these **recommended scopes**:
   - ✅ **View and manage all orders** (required)
   - ✅ **View all store information** (required)
   - ✅ **View and manage all store files** (required)
   - ✅ **View all store products** (recommended)
3. Copy your API key

**Access Level:** Choose "Account (all stores)" for maximum flexibility.

📖 **Detailed guide:** See [API_TOKEN_SETUP.md](API_TOKEN_SETUP.md) for complete instructions and security tips.

### 2. Install the MCP Server

```bash
cd /Users/gianni-dalerta/Projects/Purple-Horizons/printful-ph-mcp
pip install -e .
```

### 3. Configure Cursor

Add this to your Cursor MCP settings file:

**Location:** `~/.cursor/mcp.json` or workspace `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "printful": {
      "command": "python",
      "args": ["-m", "printful_mcp"],
      "cwd": "/Users/gianni-dalerta/Projects/Purple-Horizons/printful-ph-mcp",
      "env": {
        "PRINTFUL_API_KEY": "paste-your-api-key-here"
      }
    }
  }
}
```

**That's it!** Restart Cursor and you'll have access to all Printful tools.

## First Commands to Try

Once configured, try these in Cursor:

1. **Browse products:**
   - "Show me available t-shirts in the catalog"
   - Uses `printful_list_catalog_products`

2. **Get product details:**
   - "Get details for product ID 71"
   - Uses `printful_get_product`

3. **Check pricing:**
   - "What's the price for variant 4011?"
   - Uses `printful_get_variant_prices`

4. **List stores:**
   - "Show my Printful stores"
   - Uses `printful_list_stores`

## Common Workflows

### Workflow 1: Create an Order

```
1. Browse catalog → Find product ID
2. Get variants → Find variant ID (size/color)
3. Create order → Gets order ID
4. Add items to order (via create with items)
5. Confirm order → Starts fulfillment
```

### Workflow 2: Generate Mockups

```
1. Get product → Find mockup style IDs
2. Upload design → Get file URL
3. Create mockup task → Get task ID
4. Check task status → Get mockup URLs
```

## Troubleshooting

**Server not showing in Cursor:**
- Restart Cursor completely
- Check that API key is set in config
- Verify Python path with `which python`

**"PRINTFUL_API_KEY required" error:**
- Ensure API key is in the `env` section of MCP config
- API key should NOT have quotes in the JSON config

**Rate limit errors:**
- v2 API allows 120 requests/minute
- Wait time shown in error message
- Implement request batching if needed

## What's Using v1 vs v2?

**v2 (Primary):**
- ✅ Catalog, Orders, Shipping, Mockups, Files, Stores, Webhooks

**v1 (Fallback):**
- ⚠️ Sync Products only (not yet in v2)

The server automatically uses the right version for each feature.
