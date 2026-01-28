#!/bin/bash
# Test the Printful MCP server with MCP Inspector

echo "Starting MCP Inspector..."
echo "This will open a web UI at http://localhost:5173"
echo ""
echo "Make sure you have set PRINTFUL_API_KEY in your environment:"
echo "  export PRINTFUL_API_KEY=your-api-key-here"
echo ""

# Run MCP Inspector
npx @modelcontextprotocol/inspector python -m printful_mcp
