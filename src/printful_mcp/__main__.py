"""Allow running the package as a module: python -m printful_mcp"""

import argparse
import os
import sys


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Printful MCP Server")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport type: stdio (default, for Cursor/Claude), http (for HTTP clients), sse (legacy)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind HTTP server (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP server (default: 8000)"
    )
    return parser.parse_args()


def main():
    """Entry point for the MCP server."""
    args = parse_args()
    
    # Import server module
    from .server import mcp
    
    # Check for API key
    if not os.getenv("PRINTFUL_API_KEY"):
        print("Error: PRINTFUL_API_KEY environment variable is required", file=sys.stderr)
        print("Get your API key from: https://www.printful.com/dashboard/api", file=sys.stderr)
        sys.exit(1)
    
    # Configure HTTP settings by modifying mcp.settings directly
    if args.transport in ("http", "sse"):
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        print(f"Starting {args.transport.upper()} server on http://{args.host}:{args.port}", file=sys.stderr)
    
    # Run the server with selected transport
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "http":
        mcp.run(transport="streamable-http")
    elif args.transport == "sse":
        mcp.run(transport="sse")


if __name__ == "__main__":
    main()
