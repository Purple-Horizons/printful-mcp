# API Token Setup Guide

## Creating Your Printful API Token

This guide explains how to create an API token with the correct scopes for the Printful MCP server.

## Step-by-Step Instructions

### 1. Access the API Settings

1. Log in to your Printful account
2. Go to https://www.printful.com/dashboard/api
3. Click **"Create API Application"** or **"Create Token"**

### 2. Choose Access Level

You'll see two options:

#### Option A: Account (all stores) - **RECOMMENDED**
- ✅ Choose this if you have or plan to have multiple stores
- ✅ More flexible - works across all your stores
- ✅ Can specify individual stores with `PRINTFUL_STORE_ID` env var

#### Option B: A single store
- Use only if you work with one store and won't add more
- More restrictive but slightly more secure

**Recommendation:** Use **Account (all stores)** for maximum flexibility.

---

### 3. Select Scopes

Scopes control what the API token can do. Here's what you need:

## Essential Scopes (Required)

### ✅ Orders: "View and manage all orders"
**Why needed:**
- Create draft orders
- View order status
- Confirm orders for fulfillment
- List all orders

**Tools that need this:**
- `printful_create_order`
- `printful_get_order`
- `printful_confirm_order`
- `printful_list_orders`

### ✅ Store Information: "View all store information"
**Why needed:**
- List available stores
- Get store statistics
- Access store metadata

**Tools that need this:**
- `printful_list_stores`
- `printful_get_store_stats`

### ✅ Files: "View and manage all store files"
**Why needed:**
- Upload design files
- Retrieve file information
- Generate mockups with custom designs

**Tools that need this:**
- `printful_add_file`
- `printful_get_file`
- `printful_create_mockup_task`

---

## Recommended Scopes

### ✅ Store Products: "View all store products"
**Why needed:**
- Access sync products (pre-configured templates)
- View product configurations
- List saved designs

**Tools that need this:**
- `printful_list_sync_products` (v1 API)
- `printful_get_sync_product` (v1 API)

**Note:** Use "View" instead of "View and manage" if you only need to read sync products.

---

## Optional Scopes

### ⚪ Webhooks: "View webhooks" or "View and manage webhooks"
**Why needed:**
- Only if you plan to manage webhook configurations
- Not needed for core functionality

**Current status:** Webhook tools not implemented yet

### ⚪ Product Templates: "View product templates"
**Why needed:**
- Legacy v1 API feature
- Not commonly used
- Product templates are being deprecated

**Recommendation:** Skip unless you specifically need this

---

## Scope Combinations by Use Case

### Use Case 1: Full Functionality (Recommended)
**Perfect for:** Complete access to all features

```
✅ View and manage all orders
✅ View all store information  
✅ View and manage all store files
✅ View all store products
```

### Use Case 2: Read-Only Testing
**Perfect for:** Testing, browsing catalog, viewing data

```
✅ View all orders (read-only version if available)
✅ View all store information
✅ View all store files (read-only version if available)
```

### Use Case 3: Order Creation Only
**Perfect for:** E-commerce integrations that only create orders

```
✅ View and manage all orders
✅ View all store information
✅ View and manage all store files
```

### Use Case 4: Catalog & Mockups Only
**Perfect for:** Product browsing and mockup generation

```
✅ View all store information
✅ View and manage all store files
⚪ View all store products (optional)
```

---

## Security Best Practices

### 🔒 Token Security

1. **Never commit tokens to git**
   - Use `.env` files (already in `.gitignore`)
   - Use environment variables

2. **Use minimal required scopes**
   - Don't grant "manage" if "view" is sufficient
   - Review your needs before selecting scopes

3. **Rotate tokens periodically**
   - Create new tokens every 3-6 months
   - Revoke old tokens after migration

4. **One token per project**
   - Don't share tokens across projects
   - Easier to revoke if compromised

5. **Monitor token usage**
   - Check Printful dashboard for API activity
   - Investigate suspicious patterns

### 🚨 If Token is Compromised

If you accidentally expose your API token:

1. **Immediately revoke it** at https://www.printful.com/dashboard/api
2. **Create a new token** with fresh credentials
3. **Update your `.env` file** with the new token
4. **Restart your MCP server** to use the new token
5. **Review recent API activity** in Printful dashboard

---

## Setting Up the Token

### Method 1: Environment File (Recommended)

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your token:
```bash
PRINTFUL_API_KEY=your-actual-token-here

# Optional: For account-level tokens
# PRINTFUL_STORE_ID=12345
```

3. The `.env` file is automatically ignored by git ✅

### Method 2: Direct in MCP Config

For Cursor (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "printful": {
      "command": "python",
      "args": ["-m", "printful_mcp"],
      "cwd": "/path/to/printful-ph-mcp",
      "env": {
        "PRINTFUL_API_KEY": "your-actual-token-here"
      }
    }
  }
}
```

For Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "printful": {
      "command": "python",
      "args": ["-m", "printful_mcp"],
      "cwd": "/path/to/printful-ph-mcp",
      "env": {
        "PRINTFUL_API_KEY": "your-actual-token-here"
      }
    }
  }
}
```

### Method 3: Export in Shell (Temporary)

For testing only:
```bash
export PRINTFUL_API_KEY=your-actual-token-here
python test_server.py
```

**Note:** This only lasts for your current terminal session.

---

## Troubleshooting

### "PRINTFUL_API_KEY environment variable is required"

**Cause:** Token not set or not accessible

**Solutions:**
1. Check `.env` file exists and has the key
2. Verify no typos in variable name
3. For MCP configs, check JSON syntax
4. Restart Cursor/Claude Desktop completely

### "Unauthorized" or "403 Forbidden"

**Cause:** Invalid token or insufficient scopes

**Solutions:**
1. Verify token is correct (copy-paste from Printful dashboard)
2. Check token hasn't been revoked
3. Verify required scopes are enabled
4. Try creating a new token with all recommended scopes

### "Rate limit exceeded"

**Cause:** Too many API requests (normal behavior)

**Solutions:**
1. Wait 60 seconds and try again
2. Printful v2 API allows 120 requests/minute
3. This is expected - the MCP server handles it gracefully

---

## Testing Your Token

After setting up your token, test it:

```bash
# Set your token
export PRINTFUL_API_KEY=your-token-here

# Run the test suite
python test_server.py
```

Expected output:
```
✓ PASS - Connection & Auth
✓ PASS - List Countries
✓ PASS - List Products
...
```

If all tests pass, your token is configured correctly! 🎉

---

## Summary

### Recommended Setup
```
Access Level: Account (all stores)

Scopes:
✅ View and manage all orders
✅ View all store information
✅ View and manage all store files
✅ View all store products

Security:
🔒 Store in .env file (never commit)
🔒 Use minimal scopes needed
🔒 Rotate every 3-6 months
```

### Quick Checklist
- [ ] Created API token at https://www.printful.com/dashboard/api
- [ ] Selected "Account (all stores)" access level
- [ ] Enabled all recommended scopes
- [ ] Added token to `.env` file
- [ ] Verified `.env` is in `.gitignore`
- [ ] Tested with `python test_server.py`
- [ ] Configured Cursor/Claude Desktop MCP

---

## Need Help?

- **Printful API Docs:** https://developers.printful.com/docs/
- **Create API Token:** https://www.printful.com/dashboard/api
- **Project Issues:** [GitHub Issues](https://github.com/Purple-Horizons/printful-mcp/issues)
