# Testing Guide for Printful MCP Server

## Prerequisites

Before testing, you need:
1. **Printful API Key** - Get from https://www.printful.com/dashboard/api
2. **Python 3.10+** installed
3. **Package installed** - Run `pip install -e .` from project root

## Method 1: MCP Inspector (Fastest - Recommended)

The MCP Inspector provides a web UI to test your tools interactively.

### Setup

```bash
# Set your API key
export PRINTFUL_API_KEY=your-api-key-here

# Run the inspector (will install if needed)
npx @modelcontextprotocol/inspector python -m printful_mcp
```

Or use the provided script:
```bash
./test-with-inspector.sh
```

### What You'll See

- Opens browser at `http://localhost:5173`
- Lists all 17 tools with descriptions
- Click any tool to see input parameters
- Fill in parameters and click "Run"
- See real-time responses

### Test Cases to Try

1. **List Products** (Read-only, safe)
   - Tool: `printful_list_catalog_products`
   - Params: `limit=5`, `format=markdown`
   - Should return catalog products

2. **Get Product Details** (Read-only, safe)
   - Tool: `printful_get_product`
   - Params: `product_id=71`, `format=markdown`
   - Should return product info

3. **List Countries** (Read-only, safe)
   - Tool: `printful_list_countries`
   - No params needed
   - Should return country list

## Method 2: Test in Cursor (Full Integration)

### Setup Cursor

1. **Create/Edit** `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "printful": {
      "command": "python",
      "args": ["-m", "printful_mcp"],
      "cwd": "/Users/gianni-dalerta/Projects/Purple-Horizons/printful-ph-mcp",
      "env": {
        "PRINTFUL_API_KEY": "your-actual-api-key"
      }
    }
  }
}
```

2. **Restart Cursor completely** (Cmd+Q, then reopen)

3. **Verify Connection**:
   - Look for MCP icon in Cursor
   - Should show "printful" server connected

### Test Queries

Try these prompts in Cursor:

**Safe Read-Only Tests:**
```
1. "Show me 5 t-shirts from the Printful catalog"
2. "What are the details of Printful product 71?"
3. "List all countries where Printful ships"
4. "Show me my Printful stores"
```

**Order Creation Tests (Creates Draft Orders):**
```
5. "Create a draft order for John Doe at 123 Main St, Los Angeles, CA 90001"
   (Note: Draft orders don't charge anything)
```

## Method 3: Manual Python Testing

### Create a Test Script

```python
# test_manual.py
import asyncio
import os
from printful_mcp.client import PrintfulClient
from printful_mcp.models.inputs import ListCatalogProductsInput
from printful_mcp.tools.catalog import list_catalog_products

async def test_catalog():
    # Set your API key
    os.environ['PRINTFUL_API_KEY'] = 'your-api-key-here'
    
    # Create client
    client = PrintfulClient()
    
    try:
        # Test listing products
        params = ListCatalogProductsInput(
            limit=5,
            format="markdown"
        )
        result = await list_catalog_products(client, params)
        print(result)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_catalog())
```

Run it:
```bash
python test_manual.py
```

## Method 4: Unit Tests (Development)

### Create Test Suite

```python
# tests/test_client.py
import pytest
from printful_mcp.client import PrintfulClient, PrintfulAPIError

def test_client_requires_api_key(monkeypatch):
    """Test that client fails without API key."""
    monkeypatch.delenv("PRINTFUL_API_KEY", raising=False)
    with pytest.raises(ValueError, match="PRINTFUL_API_KEY"):
        PrintfulClient()

@pytest.mark.asyncio
async def test_client_makes_request(monkeypatch):
    """Test that client can make requests."""
    monkeypatch.setenv("PRINTFUL_API_KEY", "test-key")
    client = PrintfulClient()
    # Add mock tests here
    await client.close()
```

Run tests:
```bash
pip install -e ".[dev]"
pytest tests/
```

## Method 5: Live API Testing

### Test with Real Printful API

**⚠️ Warning:** These interact with your real Printful account.

#### Safe Read-Only Tests

```bash
# Set API key
export PRINTFUL_API_KEY=your-api-key

# Test 1: List products (safe)
python -c "
import asyncio
from printful_mcp.client import PrintfulClient

async def test():
    client = PrintfulClient()
    result = await client.get('/catalog-products', params={'limit': 3})
    print(result)
    await client.close()

asyncio.run(test())
"
```

#### Test Order Creation (Creates Draft)

```python
# This creates a DRAFT order (not charged)
import asyncio
from printful_mcp.client import PrintfulClient

async def test_order():
    client = PrintfulClient()
    try:
        order_data = {
            "recipient": {
                "name": "Test User",
                "address1": "123 Test St",
                "city": "Los Angeles",
                "state_code": "CA",
                "country_code": "US",
                "zip": "90001"
            },
            "external_id": "test-order-123"
        }
        result = await client.post('/orders', json_data=order_data)
        print(f"Created draft order: {result['data']['id']}")
    finally:
        await client.close()

asyncio.run(test_order())
```

## Recommended Testing Flow

### Phase 1: Basic Functionality ✓
1. Use MCP Inspector to test a few read-only tools
2. Verify error handling (try invalid product IDs)
3. Check rate limiting (make many requests quickly)

### Phase 2: Integration Testing ✓
1. Configure in Cursor
2. Test with natural language queries
3. Verify markdown formatting looks good
4. Test JSON format output

### Phase 3: Advanced Features ✓
1. Test order creation (draft only)
2. Test mockup generation
3. Test file uploads
4. Test sync products (v1 fallback)

## Troubleshooting Tests

### "Error: PRINTFUL_API_KEY environment variable is required"
✅ **Solution:** Make sure API key is set:
```bash
export PRINTFUL_API_KEY=your-key
```

### "Module not found: printful_mcp"
✅ **Solution:** Install the package:
```bash
pip install -e .
```

### "Connection refused" in Cursor
✅ **Solution:**
1. Check MCP config file syntax (valid JSON)
2. Restart Cursor completely
3. Check logs: `~/.cursor/logs/`

### "Rate limit exceeded"
✅ **Expected:** Printful allows 120 req/min
- Wait as indicated in error message
- This proves rate limiting detection works!

### "Invalid product ID"
✅ **Expected:** Tests error handling
- Try valid IDs: 71, 19, 77
- Error message should be clear and actionable

## Sample Test Session

Here's a complete test session you can run:

```bash
# 1. Set API key
export PRINTFUL_API_KEY=your-api-key-here

# 2. Test server starts
python -m printful_mcp
# Should NOT error (before it did without API key)

# 3. Run MCP Inspector
npx @modelcontextprotocol/inspector python -m printful_mcp

# 4. In the web UI, test these in order:
# - printful_list_countries (should return ~200 countries)
# - printful_list_catalog_products (limit=3, should show 3 products)
# - printful_get_product (product_id=71, should show t-shirt details)
# - printful_list_stores (should show your stores)

# 5. Test error handling:
# - printful_get_product (product_id=999999, should error gracefully)
```

## Success Criteria

Your MCP server is working correctly if:

- ✅ Server starts without errors (with API key set)
- ✅ MCP Inspector shows all 17 tools
- ✅ Read-only tools return data from Printful
- ✅ Invalid inputs show clear error messages
- ✅ Rate limiting is detected and handled
- ✅ Both markdown and JSON formats work
- ✅ Cursor integration shows tools in autocomplete
- ✅ Natural language queries trigger correct tools

## Next Steps After Testing

Once basic tests pass:

1. **Add to GitHub** - Push your tested code
2. **Document edge cases** - Note any API quirks you found
3. **Create issues** - For any bugs or enhancements
4. **Share with team** - Deploy to production use

## Questions?

Common questions during testing:

**Q: Will testing cost money?**
A: Read-only operations are free. Draft orders don't charge. Only confirmed orders cost money.

**Q: Can I test without a real API key?**
A: No, you need a real Printful account and API key. They have a free tier.

**Q: What if I hit rate limits?**
A: Wait as indicated. v2 API allows 120 requests per minute.

**Q: Can I test in a sandbox?**
A: Printful doesn't have a sandbox. Use draft orders (not confirmed) for testing.

**Q: How do I see MCP server logs?**
A: Check stderr output when running via inspector, or Cursor logs at `~/.cursor/logs/`
