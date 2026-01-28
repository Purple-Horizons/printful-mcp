#!/usr/bin/env python3
"""
Quick test script for Printful MCP Server.
Tests basic functionality without needing Cursor/Claude Desktop.
"""

import asyncio
import os
import sys
from printful_mcp.client import PrintfulClient, PrintfulAPIError
from printful_mcp.models.inputs import (
    ListCatalogProductsInput,
    GetProductInput,
)
from printful_mcp.tools.catalog import list_catalog_products, get_product
from printful_mcp.tools.shipping import list_countries


async def test_connection():
    """Test 1: Basic connection and authentication."""
    print("=" * 60)
    print("TEST 1: Connection & Authentication")
    print("=" * 60)
    
    try:
        client = PrintfulClient()
        print("✓ Client initialized successfully")
        print(f"✓ API Key present: {client.api_key[:10]}...")
        await client.close()
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


async def test_list_countries():
    """Test 2: List countries (simple read-only operation)."""
    print("\n" + "=" * 60)
    print("TEST 2: List Countries (Read-Only)")
    print("=" * 60)
    
    client = PrintfulClient()
    try:
        result = await list_countries(client)
        
        if "Available Countries" in result and "Error" not in result:
            print("✓ Successfully retrieved countries")
            lines = result.split('\n')
            print(f"✓ Response has {len(lines)} lines")
            print("\nFirst few lines:")
            print('\n'.join(lines[:10]))
            return True
        else:
            print(f"✗ Unexpected response: {result[:200]}")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    finally:
        await client.close()


async def test_list_products():
    """Test 3: List catalog products."""
    print("\n" + "=" * 60)
    print("TEST 3: List Catalog Products")
    print("=" * 60)
    
    client = PrintfulClient()
    try:
        params = ListCatalogProductsInput(
            limit=3,
            format="markdown"
        )
        result = await list_catalog_products(client, params)
        
        if "Catalog Products" in result and "Error" not in result:
            print("✓ Successfully retrieved products")
            print(f"✓ Response length: {len(result)} chars")
            print("\nFirst 500 chars:")
            print(result[:500])
            return True
        else:
            print(f"✗ Unexpected response: {result[:200]}")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    finally:
        await client.close()


async def test_get_product():
    """Test 4: Get specific product details."""
    print("\n" + "=" * 60)
    print("TEST 4: Get Product Details (Product ID: 71)")
    print("=" * 60)
    
    client = PrintfulClient()
    try:
        params = GetProductInput(
            product_id=71,
            format="markdown"
        )
        result = await get_product(client, params)
        
        if "#" in result and "Error" not in result:
            print("✓ Successfully retrieved product details")
            print(f"✓ Response length: {len(result)} chars")
            print("\nFirst 500 chars:")
            print(result[:500])
            return True
        else:
            print(f"✗ Unexpected response: {result[:200]}")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    finally:
        await client.close()


async def test_error_handling():
    """Test 5: Error handling with invalid product ID."""
    print("\n" + "=" * 60)
    print("TEST 5: Error Handling (Invalid Product ID)")
    print("=" * 60)
    
    client = PrintfulClient()
    try:
        params = GetProductInput(
            product_id=999999,  # Invalid ID
            format="markdown"
        )
        result = await get_product(client, params)
        
        if "Error" in result:
            print("✓ Error handled gracefully")
            print(f"✓ Error message: {result[:200]}")
            return True
        else:
            print("✗ Should have returned an error")
            return False
    except Exception as e:
        # This is also acceptable - error was raised
        print(f"✓ Error raised as expected: {type(e).__name__}")
        return True
    finally:
        await client.close()


async def test_json_format():
    """Test 6: JSON format output."""
    print("\n" + "=" * 60)
    print("TEST 6: JSON Format Output")
    print("=" * 60)
    
    client = PrintfulClient()
    try:
        params = ListCatalogProductsInput(
            limit=1,
            format="json"
        )
        result = await list_catalog_products(client, params)
        
        if result.startswith('{') or result.startswith('['):
            print("✓ JSON format returned")
            print(f"✓ Response length: {len(result)} chars")
            print("\nFirst 300 chars:")
            print(result[:300])
            return True
        else:
            print(f"✗ Expected JSON, got: {result[:100]}")
            return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    finally:
        await client.close()


async def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 60)
    print("PRINTFUL MCP SERVER - TEST SUITE")
    print("=" * 60)
    print("\nThis will test the MCP server with the Printful API.")
    print("Make sure PRINTFUL_API_KEY is set in your environment.\n")
    
    # Check API key
    api_key = os.getenv("PRINTFUL_API_KEY")
    if not api_key:
        print("ERROR: PRINTFUL_API_KEY environment variable not set!")
        print("\nTo set it, run:")
        print("  export PRINTFUL_API_KEY=your-api-key-here")
        print("\nGet your API key from: https://www.printful.com/dashboard/api")
        sys.exit(1)
    
    print(f"Using API key: {api_key[:10]}...\n")
    
    # Run tests
    tests = [
        ("Connection & Auth", test_connection),
        ("List Countries", test_list_countries),
        ("List Products", test_list_products),
        ("Get Product", test_get_product),
        ("Error Handling", test_error_handling),
        ("JSON Format", test_json_format),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your MCP server is working correctly.")
        print("\nNext steps:")
        print("1. Try the MCP Inspector: ./test-with-inspector.sh")
        print("2. Configure Cursor and test with natural language")
        print("3. See TESTING.md for more advanced tests")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
