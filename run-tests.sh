#!/bin/bash
# Full test suite runner

echo "🧪 Printful MCP Server - Full Test Suite"
echo "=========================================="
echo ""

# Check for API key in .env
if [ -f .env ]; then
    echo "✓ Found .env file"
    source .env
else
    echo "⚠️  No .env file found"
fi

# Check API key is set
if [ -z "$PRINTFUL_API_KEY" ]; then
    echo ""
    echo "❌ ERROR: PRINTFUL_API_KEY not set!"
    echo ""
    echo "Options:"
    echo "  1. Create .env file: cp .env.example .env (then edit it)"
    echo "  2. Export directly: export PRINTFUL_API_KEY=your-key"
    echo ""
    exit 1
fi

echo "✓ API Key set: ${PRINTFUL_API_KEY:0:10}..."
echo ""

# Menu
echo "Select test suite:"
echo "  1) Quick test (6 tests, ~3 seconds)"
echo "  2) Comprehensive test (19 tools, ~5 seconds)"
echo "  3) Both"
echo "  4) MCP Inspector (interactive web UI)"
echo ""
read -p "Choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Running quick test suite..."
        python test_server.py
        ;;
    2)
        echo ""
        echo "Running comprehensive test suite..."
        python test_comprehensive.py
        ;;
    3)
        echo ""
        echo "Running quick test suite..."
        python test_server.py
        echo ""
        echo "Running comprehensive test suite..."
        python test_comprehensive.py
        ;;
    4)
        echo ""
        echo "Launching MCP Inspector..."
        echo "This will open a browser at http://localhost:5173"
        echo ""
        npx @modelcontextprotocol/inspector python -m printful_mcp
        ;;
    *)
        echo "Invalid choice. Run again and choose 1-4."
        exit 1
        ;;
esac
