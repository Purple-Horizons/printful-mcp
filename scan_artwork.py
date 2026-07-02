#!/usr/bin/env python3
"""
Scan all sync products in a store and report which have real uploaded artwork
files versus parametric designs (text / clipart with no source file).

Printful sync variants describe each design as a set of placement layers. An
uploaded image/vector carries a non-empty layer ``url``; text ("textbox") and
"clipart" layers are generated in Printful's design maker and have no file URL.
This script fetches every sync product's variants via the v2 API and flags any
non-empty layer URLs as real artwork.

Usage:
    PRINTFUL_API_KEY=... PRINTFUL_STORE_ID=... python scan_artwork.py

The store ID is read from PRINTFUL_STORE_ID (required for account-level tokens)
or can be passed as the first CLI argument.
"""

import asyncio
import os
import sys

from src.printful_mcp.client import PrintfulClient, PrintfulAPIError


async def scan(client: PrintfulClient) -> int:
    products = (await client.get("/sync-products", version="v2", params={"limit": 100})).get("data", [])
    print(f"Scanning {len(products)} sync products...\n")

    real_count = 0
    for product in products:
        pid = product["id"]
        variants = (
            await client.get(
                f"/sync-products/{pid}/sync-variants",
                version="v2",
                params={"limit": 100},
            )
        ).get("data", [])

        techniques: set[str] = set()
        layer_types: set[str] = set()
        artwork_urls: set[str] = set()
        for variant in variants:
            for placement in variant.get("placements", []):
                if placement.get("technique"):
                    techniques.add(placement["technique"])
                for layer in placement.get("layers", []):
                    if layer.get("type"):
                        layer_types.add(layer["type"])
                    if layer.get("url"):
                        artwork_urls.add(layer["url"])

        has_artwork = bool(artwork_urls)
        real_count += has_artwork
        verdict = "REAL ARTWORK" if has_artwork else "parametric/no file"
        print(f"[{verdict}] {product.get('name', 'Unnamed')}  (id {pid}, {len(variants)} variants)")
        print(f"    technique(s): {sorted(techniques)}  layer type(s): {sorted(layer_types)}")
        for url in sorted(artwork_urls):
            print(f"    ARTWORK URL: {url}")
        print()

    print(f"Done: {real_count} of {len(products)} products have real uploaded artwork.")
    return real_count


async def main() -> None:
    store_id = sys.argv[1] if len(sys.argv) > 1 else os.getenv("PRINTFUL_STORE_ID")
    client = PrintfulClient(store_id=store_id)
    try:
        await scan(client)
    except PrintfulAPIError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        sys.exit(1)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
