#!/usr/bin/env python3
"""
COMPLETE TEST SUITE - Tests ALL 17 tools with real data
Uses printthis.art store (ID: 14690720)
"""

import asyncio
import os
import sys
import json
from datetime import datetime, timedelta
from printful_mcp.client import PrintfulClient
from printful_mcp.models.inputs import *
from printful_mcp.tools import catalog, orders, shipping, mockups, files, stores, sync

STORE_ID = "14690720"  # Printthis.art
TEST_ORDER_EXTERNAL_ID = f"mcp-test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

print("="*70)
print("COMPLETE PRINTFUL MCP TEST SUITE")
print("="*70)
print(f"\nUsing Store: Printthis.art (ID: {STORE_ID})")
print(f"Test Order ID: {TEST_ORDER_EXTERNAL_ID}")
print("\n⚠️  This will create TEST DATA in your Printful account:")
print("  - 1 draft order (not charged)")
print("  - 1 test file upload")
print("  - Store statistics query")
print("  - Shipping calculation")
print("\n")

async def test_complete():
    """Run complete test suite."""
    
    # Set store ID in environment
    os.environ['PRINTFUL_STORE_ID'] = STORE_ID
    
    results = []
    client = PrintfulClient(store_id=STORE_ID)
    
    try:
        # ==================== CATALOG TOOLS ====================
        print("\n" + "="*70)
        print("CATALOG TOOLS (5 tests)")
        print("="*70)
        
        # Test 1: List products
        print("\n1/17: printful_list_catalog_products")
        params = ListCatalogProductsInput(limit=3, format="markdown")
        result = await catalog.list_catalog_products(client, params)
        success = "Catalog Products" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        if success:
            print(f"   Found products in catalog")
        results.append(("list_catalog_products", success))
        
        # Test 2: Get product
        print("\n2/17: printful_get_product")
        params = GetProductInput(product_id=71, format="markdown")
        result = await catalog.get_product(client, params)
        success = "Unisex" in result or "T-Shirt" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        results.append(("get_product", success))
        
        # Test 3: Get variants
        print("\n3/17: printful_get_product_variants")
        params = GetProductVariantsInput(product_id=71, limit=3, format="markdown")
        result = await catalog.get_product_variants(client, params)
        success = "Variant" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        results.append(("get_product_variants", success))
        
        # Test 4: Get prices
        print("\n4/17: printful_get_variant_prices")
        params = GetVariantPricesInput(variant_id=4011, currency="USD", format="markdown")
        result = await catalog.get_variant_prices(client, params)
        success = "Pricing" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        results.append(("get_variant_prices", success))
        
        # Test 5: Get availability
        print("\n5/17: printful_get_product_availability")
        params = GetProductAvailabilityInput(product_id=71, format="markdown")
        result = await catalog.get_product_availability(client, params)
        success = "Availability" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        results.append(("get_product_availability", success))
        
        # ==================== SHIPPING TOOLS ====================
        print("\n" + "="*70)
        print("SHIPPING TOOLS (2 tests)")
        print("="*70)
        
        # Test 6: List countries
        print("\n6/17: printful_list_countries")
        result = await shipping.list_countries(client)
        success = "Available Countries" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        results.append(("list_countries", success))
        
        # Test 7: Calculate shipping
        print("\n7/17: printful_calculate_shipping")
        items_json = json.dumps([{
            "catalog_variant_id": 4011,
            "quantity": 1,
            "source": "catalog",
            "placements": [{
                "placement": "front",
                "technique": "dtg",
                "layers": [{
                    "type": "file",
                    "url": "https://via.placeholder.com/500x500.png"
                }]
            }]
        }])
        params = CalculateShippingInput(
            recipient_country_code="US",
            recipient_state_code="CA",
            recipient_city="Los Angeles",
            recipient_zip="90001",
            items_json=items_json,
            format="markdown"
        )
        result = await shipping.calculate_shipping_rates(client, params)
        success = "Shipping Rates" in result or "shipping" in result.lower()
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        if success:
            print(f"   Calculated rates for LA delivery")
        results.append(("calculate_shipping", success))
        
        # ==================== STORE TOOLS ====================
        print("\n" + "="*70)
        print("STORE TOOLS (2 tests)")
        print("="*70)
        
        # Test 8: List stores
        print("\n8/17: printful_list_stores")
        params = ListStoresInput(format="markdown")
        result = await stores.list_stores(client, params)
        success = "Stores" in result and "Printthis.art" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        results.append(("list_stores", success))
        
        # Test 9: Get store stats
        print("\n9/17: printful_get_store_stats")
        date_to = datetime.now().strftime("%Y-%m-%d")
        date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        params = GetStoreStatsInput(
            store_id=int(STORE_ID),
            date_from=date_from,
            date_to=date_to,
            report_types="sales_and_costs,profit",
            format="markdown"
        )
        result = await stores.get_store_statistics(client, params)
        success = "Statistics" in result or "Profit" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        if success:
            print(f"   Retrieved stats for {date_from} to {date_to}")
        results.append(("get_store_stats", success))
        
        # ==================== ORDER TOOLS ====================
        print("\n" + "="*70)
        print("ORDER TOOLS (4 tests)")
        print("="*70)
        
        # Test 10: Create order
        print("\n10/17: printful_create_order (CREATES DRAFT)")
        params = CreateOrderInput(
            recipient_name="MCP Test User",
            recipient_address1="123 Test Street",
            recipient_city="Los Angeles",
            recipient_state_code="CA",
            recipient_country_code="US",
            recipient_zip="90001",
            recipient_email="test@example.com",
            external_id=TEST_ORDER_EXTERNAL_ID,
            format="json"
        )
        result = await orders.create_order(client, params)
        success = "id" in result.lower() and "error" not in result.lower()
        created_order_id = None
        if success:
            try:
                data = json.loads(result)
                created_order_id = data.get('data', {}).get('id')
                print(f"   ✓ PASS - Created draft order: {created_order_id}")
            except:
                print(f"   ✓ PASS - Order created")
        else:
            print(f"   ✗ FAIL")
        results.append(("create_order", success))
        
        # Test 11: List orders
        print("\n11/17: printful_list_orders")
        params = ListOrdersInput(limit=5, format="markdown")
        result = await orders.list_orders(client, params)
        success = "Orders" in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        if success and TEST_ORDER_EXTERNAL_ID in result:
            print(f"   Found our test order in list!")
        results.append(("list_orders", success))
        
        # Test 12: Get order
        print("\n12/17: printful_get_order")
        if created_order_id:
            params = GetOrderInput(order_id=str(created_order_id), format="markdown")
            result = await orders.get_order(client, params)
            success = "Order" in result and str(created_order_id) in result
            print(f"   {'✓ PASS' if success else '✗ FAIL'}")
            if success:
                print(f"   Retrieved order {created_order_id}")
        else:
            print(f"   ⚠️  SKIP - No order ID from creation")
            success = None
        results.append(("get_order", success))
        
        # Test 13: Confirm order (SKIP - would charge!)
        print("\n13/17: printful_confirm_order")
        print(f"   ⚠️  SKIP - Would charge money! Draft order stays as draft.")
        results.append(("confirm_order", None))
        
        # ==================== FILE TOOLS ====================
        print("\n" + "="*70)
        print("FILE TOOLS (2 tests)")
        print("="*70)
        
        # Test 14: Add file
        print("\n14/17: printful_add_file (UPLOADS FILE)")
        params = AddFileInput(
            url="https://via.placeholder.com/500x500.png",
            filename="mcp-test-file.png",
            visible=False,
            format="json"
        )
        result = await files.add_file(client, params)
        success = "id" in result.lower() and "error" not in result.lower()
        uploaded_file_id = None
        if success:
            try:
                data = json.loads(result)
                uploaded_file_id = data.get('data', {}).get('id')
                print(f"   ✓ PASS - Uploaded file: {uploaded_file_id}")
            except:
                print(f"   ✓ PASS - File uploaded")
        else:
            print(f"   ✗ FAIL")
        results.append(("add_file", success))
        
        # Test 15: Get file
        print("\n15/17: printful_get_file")
        if uploaded_file_id:
            params = GetFileInput(file_id=uploaded_file_id, format="markdown")
            result = await files.get_file(client, params)
            success = "File" in result and str(uploaded_file_id) in result
            print(f"   {'✓ PASS' if success else '✗ FAIL'}")
            if success:
                print(f"   Retrieved file {uploaded_file_id}")
        else:
            print(f"   ⚠️  SKIP - No file ID from upload")
            success = None
        results.append(("get_file", success))
        
        # ==================== MOCKUP TOOLS ====================
        print("\n" + "="*70)
        print("MOCKUP TOOLS (2 tests) - SKIPPED")
        print("="*70)
        
        print("\n16/17: printful_create_mockup_task")
        print(f"   ⚠️  SKIP - Uses API credits, skip for test")
        results.append(("create_mockup_task", None))
        
        print("\n17/17: printful_get_mockup_task")
        print(f"   ⚠️  SKIP - No mockup task created")
        results.append(("get_mockup_task", None))
        
        # ==================== SYNC PRODUCTS (v1) ====================
        print("\n" + "="*70)
        print("SYNC PRODUCTS - v1 API (2 tests)")
        print("="*70)
        
        print("\n18/19: printful_list_sync_products (v1)")
        params = sync.ListSyncProductsInput(limit=5, format="markdown")
        result = await sync.list_sync_products(client, params)
        success = "Sync Products" in result and "Error" not in result
        print(f"   {'✓ PASS' if success else '✗ FAIL'}")
        if success:
            print(f"   Listed sync products from store")
        results.append(("list_sync_products", success))
        
        print("\n19/19: printful_get_sync_product (v1)")
        print(f"   ⚠️  SKIP - Need valid sync product ID")
        results.append(("get_sync_product", None))
        
    finally:
        await client.close()
    
    # ==================== SUMMARY ====================
    print("\n" + "="*70)
    print("COMPLETE TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, r in results if r is True)
    failed = sum(1 for _, r in results if r is False)
    skipped = sum(1 for _, r in results if r is None)
    total = len(results)
    
    print(f"\nResults:")
    print(f"  ✓ Passed:  {passed}/{total}")
    print(f"  ✗ Failed:  {failed}/{total}")
    print(f"  ⚠️  Skipped: {skipped}/{total}")
    
    print(f"\nDetailed Results:")
    for name, result in results:
        if result is True:
            status = "✓ PASS  "
        elif result is None:
            status = "⚠️  SKIP  "
        else:
            status = "✗ FAIL  "
        print(f"  {status} {name}")
    
    print(f"\n" + "="*70)
    if failed == 0:
        print("🎉 ALL TESTED TOOLS WORKING PERFECTLY!")
        print(f"\nTest artifacts created:")
        print(f"  - Draft order: {TEST_ORDER_EXTERNAL_ID}")
        print(f"  - Test file: mcp-test-file.png")
        print(f"\nYou can view/delete these in your Printful dashboard:")
        print(f"  https://www.printful.com/dashboard")
    else:
        print("⚠️  Some tests failed - see details above")
    print("="*70)
    
    return passed, failed, skipped

if __name__ == "__main__":
    passed, failed, skipped = asyncio.run(test_complete())
    sys.exit(0 if failed == 0 else 1)
