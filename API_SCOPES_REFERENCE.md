# API Token Scope Recommendations - Quick Reference

## TL;DR - Recommended Setup

### Access Level
```
✅ Account (all stores)  ← Choose this
⚪ A single store
```

### Required Scopes
```
✅ View and manage all orders
✅ View all store information
✅ View and manage all store files
✅ View all store products
```

### Optional (Skip These)
```
⚪ View/manage webhooks (not implemented yet)
⚪ View/manage product templates (legacy/deprecated)
```

---

## Why These Scopes?

### ✅ View and manage all orders
**Used by:** 4 tools
- `printful_create_order` - Create draft orders
- `printful_get_order` - View order details
- `printful_confirm_order` - Submit orders for fulfillment
- `printful_list_orders` - Browse all orders

**Why "manage"?** Need to create and confirm orders, not just view.

---

### ✅ View all store information
**Used by:** 2 tools
- `printful_list_stores` - List your Printful stores
- `printful_get_store_stats` - Get sales/profit metrics

**Why "view only"?** We only read store data, never modify settings.

---

### ✅ View and manage all store files
**Used by:** 3 tools
- `printful_add_file` - Upload design files
- `printful_get_file` - Check file processing status
- `printful_create_mockup_task` - Generate mockups (needs files)

**Why "manage"?** Need to upload files, not just view existing ones.

---

### ✅ View all store products
**Used by:** 2 tools (v1 API)
- `printful_list_sync_products` - List pre-configured products
- `printful_get_sync_product` - Get sync product details

**Why needed?** Access to sync products (saved product templates).

**Note:** Use "View" not "View and manage" unless you need to modify sync products.

---

## What's NOT Needed

### ⚪ Webhooks
**Not used** - Webhook configuration tools aren't implemented yet.
**Safe to skip** unless you plan to manually use webhooks.

### ⚪ Product Templates  
**Deprecated** - Old v1 API feature being phased out.
**Safe to skip** - Not used by any tools.

---

## Security Implications

### Minimum Viable Scopes (Most Restrictive)
If you only want to browse the catalog without creating orders:
```
✅ View all store information (catalog browsing uses public v2 endpoints)
```

### Read-Only Testing
For testing without making changes:
```
✅ View all orders (not "manage")
✅ View all store information
✅ View all store files (not "manage")
✅ View all store products
```

### Production Use (Recommended)
For full functionality including order creation:
```
✅ View and manage all orders
✅ View all store information
✅ View and manage all store files
✅ View all store products
```

---

## Tools by Scope Requirements

### No API Key Needed (Public Endpoints)
These use Printful's public v2 API:
- `printful_list_catalog_products`
- `printful_get_product`
- `printful_get_product_variants`
- `printful_get_variant_prices`
- `printful_get_product_availability`
- `printful_calculate_shipping`
- `printful_list_countries`

**Note:** While these work without authentication, providing an API key gives you higher rate limits.

### Requires: Orders Scope
- `printful_create_order`
- `printful_get_order`
- `printful_confirm_order`
- `printful_list_orders`

### Requires: Store Information Scope
- `printful_list_stores`
- `printful_get_store_stats`

### Requires: Files Scope
- `printful_add_file`
- `printful_get_file`
- `printful_create_mockup_task`
- `printful_get_mockup_task`

### Requires: Store Products Scope
- `printful_list_sync_products`
- `printful_get_sync_product`

---

## Common Questions

### Q: Can I use "view" instead of "view and manage"?
**A:** Yes, but you'll lose functionality:
- **Orders:** Can only view, not create/confirm
- **Files:** Can only view, not upload
- **Store Products:** Can view but not modify sync products

### Q: What's the difference between "Account" and "Single Store"?
**A:**
- **Account:** Works with all your stores, can switch between them
- **Single Store:** Locked to one store only

**Recommendation:** Use "Account" - it's more flexible and you can still specify which store with `PRINTFUL_STORE_ID`.

### Q: How do I know if my scopes are correct?
**A:** Run the test suite:
```bash
export PRINTFUL_API_KEY=your-key
python test_server.py
```

If you get permission errors, you need to add more scopes.

### Q: Can I change scopes later?
**A:** Yes! Go to https://www.printful.com/dashboard/api and edit your token's scopes, or create a new token.

---

## Quick Setup Checklist

```
[ ] Go to https://www.printful.com/dashboard/api
[ ] Click "Create API Application"
[ ] Select "Account (all stores)"
[ ] Enable these scopes:
    [ ] View and manage all orders
    [ ] View all store information
    [ ] View and manage all store files
    [ ] View all store products
[ ] Copy the API key
[ ] Add to .env file: PRINTFUL_API_KEY=...
[ ] Test: python test_server.py
```

Done! 🎉
