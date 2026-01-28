<div align="center">

# 🎨 Printful MCP Server

### **Automate Your Print-on-Demand Business with AI**

Connect Printful's powerful API to Claude, Cursor, and other AI assistants through the Model Context Protocol.

[**📚 Quick Start**](#installation) • [**🔧 Configuration**](#configuration) • [**🚀 Examples**](#usage-examples) • [**📖 Documentation**](QUICKSTART.md)

---

[![Made by Purple Horizons](https://img.shields.io/badge/Made_by-Purple_Horizons-7C3AED?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkw2IDhMMTIgMTRMMTggOEwxMiAyWiIgZmlsbD0id2hpdGUiLz48cGF0aCBkPSJNMTIgMTBMMTggMTZMMTIgMjJMNiAxNkwxMiAxMFoiIGZpbGw9IndoaXRlIi8+PC9zdmc+)](https://purplehorizons.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Printful API v2](https://img.shields.io/badge/Printful-API_v2-00A3FF?style=for-the-badge)](https://developers.printful.com/docs/v2-beta/)

[![GitHub Stars](https://img.shields.io/github/stars/Purple-Horizons/printful-ph-mcp?style=social)](https://github.com/Purple-Horizons/printful-ph-mcp)
[![GitHub Forks](https://img.shields.io/github/forks/Purple-Horizons/printful-ph-mcp?style=social)](https://github.com/Purple-Horizons/printful-ph-mcp/fork)

---

### 🎁 **New to Printful?**

<a href="https://www.printful.com/a/YOUR_AFFILIATE_ID">
  <img src="https://img.shields.io/badge/Sign_Up-Get_Started_Free-FA4616?style=for-the-badge&logo=printful&logoColor=white" alt="Sign up for Printful">
</a>

<sub>Start your print-on-demand business today • No upfront costs • 300+ products • Global fulfillment</sub>

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 **Complete API Coverage**
- ✅ Full Printful API v2 support
- ✅ Smart v1 fallback for legacy features
- ✅ 17 tools across all major domains
- ✅ Real-time stock & pricing data

</td>
<td width="50%">

### 🛡️ **Production Ready**
- ✅ Type-safe Pydantic validation
- ✅ Robust error handling
- ✅ Rate limit management
- ✅ Dual output formats (JSON/Markdown)

</td>
</tr>
<tr>
<td width="50%">

### 🚀 **Easy Integration**
- ✅ Works with Claude Desktop
- ✅ Works with Cursor IDE
- ✅ Local execution (stdio)
- ✅ No hosting required

</td>
<td width="50%">

### 🤖 **AI Skill Included**
- ✅ Cursor skill teaches AI how to use tools
- ✅ Best practices built-in
- ✅ Auto-applies workflows
- ✅ Better experience out of the box

</td>
</tr>
</table>

> **🎁 Bonus:** This repo includes a [Cursor AI skill](.cursor/skills/) that automatically teaches AI assistants how to use the Printful MCP effectively. Just open the project and start asking questions!

---

## 🚀 Quick Start

<details open>
<summary><b>📋 Prerequisites</b></summary>

<br>

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Printful API Key** ([Get one free](https://www.printful.com/dashboard/api))

</details>

<details>
<summary><b>⚡ Installation (3 steps)</b></summary>

<br>

**Step 1: Clone & Install**
```bash
git clone https://github.com/Purple-Horizons/printful-ph-mcp.git
cd printful-ph-mcp
pip install -e .
```

**Step 2: Set up API Key**
```bash
cp .env.example .env
# Edit .env and add: PRINTFUL_API_KEY=your-key-here
```

**Step 3: Configure Your AI Assistant**

<details>
<summary><b>For Cursor</b></summary>

Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "printful": {
      "command": "python",
      "args": ["-m", "printful_mcp"],
      "cwd": "/path/to/printful-ph-mcp",
      "env": {
        "PRINTFUL_API_KEY": "your-api-key-here"
      }
    }
  }
}
```
</details>

<details>
<summary><b>For Claude Desktop</b></summary>

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "printful": {
      "command": "python",
      "args": ["-m", "printful_mcp"],
      "cwd": "/path/to/printful-ph-mcp",
      "env": {
        "PRINTFUL_API_KEY": "your-api-key-here"
      }
    }
  }
}
```
</details>

✅ **That's it!** Restart your AI assistant and start using Printful tools.

</details>

---

## 🎨 What You Can Do

<div align="center">

| 🛍️ Catalog | 📦 Orders | 🚚 Shipping | 🖼️ Mockups | 📁 Files | 🏪 Stores |
|:---------:|:--------:|:----------:|:---------:|:-------:|:--------:|
| Browse 300+ products | Create & manage orders | Calculate rates | Generate mockups | Upload designs | View statistics |
| Check availability | Confirm fulfillment | List countries | Check status | Get file info | Multi-store support |
| Get pricing | Track orders | Delivery times | Custom placements | - | - |

</div>

---

## 💡 Usage Examples

### 🎯 Example 1: Find the Perfect Product

```python
# Ask your AI assistant:
"Show me all t-shirts available for DTG printing under $15"

# It will use:
printful_list_catalog_products(
    types="T-SHIRT",
    techniques="dtg",
    limit=20,
    format="markdown"
)
```

### 💰 Example 2: Get Pricing

```python
# Ask your AI assistant:
"What's the price for variant 4011 in USD?"

# It will use:
printful_get_variant_prices(
    variant_id=4011,
    currency="USD",
    format="markdown"
)
```

### 📦 Example 3: Create an Order

```python
# Ask your AI assistant:
"Create a draft order for John Doe at 123 Main St, Los Angeles, CA 90001"

# It will use:
printful_create_order(
    recipient_name="John Doe",
    recipient_address1="123 Main St",
    recipient_city="Los Angeles",
    recipient_state_code="CA",
    recipient_country_code="US",
    recipient_zip="90001"
)
```

### 🎨 Example 4: Generate Product Mockups

```python
# Ask your AI assistant:
"Generate a mockup for product 71 with my design"

# It will use:
printful_create_mockup_task(
    product_id=71,
    variant_ids="4011,4012",
    design_url="https://example.com/design.png",
    placement="front"
)
```

<div align="center">

### 🎬 **Want to see it in action?**

[📺 Watch Demo Video](#) • [📖 Read Full Documentation](QUICKSTART.md) • [💬 Join Community](#)

</div>

---

## 🛠️ Available Tools

<details>
<summary><b>🛍️ Catalog Tools (5)</b> - Browse products & check availability</summary>

<br>

| Tool | Description | Example Use |
|------|-------------|-------------|
| `printful_list_catalog_products` | Browse 300+ products with filters | "Show me all hoodies" |
| `printful_get_product` | Get detailed product info | "Tell me about product 71" |
| `printful_get_product_variants` | Get all sizes/colors | "What sizes are available?" |
| `printful_get_variant_prices` | Get pricing by currency | "How much in EUR?" |
| `printful_get_product_availability` | Check stock status | "Is this in stock?" |

</details>

<details>
<summary><b>📦 Order Tools (4)</b> - Create & manage orders</summary>

<br>

| Tool | Description | Example Use |
|------|-------------|-------------|
| `printful_create_order` | Create draft order | "Create order for John" |
| `printful_get_order` | View order details | "Show me order #12345" |
| `printful_confirm_order` | Start fulfillment | "Confirm this order" |
| `printful_list_orders` | List all orders | "Show my recent orders" |

</details>

<details>
<summary><b>🚚 Shipping Tools (2)</b> - Calculate rates & delivery</summary>

<br>

| Tool | Description | Example Use |
|------|-------------|-------------|
| `printful_calculate_shipping` | Get shipping rates & times | "How much to ship to UK?" |
| `printful_list_countries` | List supported countries | "What countries do you ship to?" |

</details>

<details>
<summary><b>🖼️ Mockup Tools (2)</b> - Generate product images</summary>

<br>

| Tool | Description | Example Use |
|------|-------------|-------------|
| `printful_create_mockup_task` | Generate mockup images | "Create mockup with my design" |
| `printful_get_mockup_task` | Check generation status | "Is my mockup ready?" |

</details>

<details>
<summary><b>📁 File Tools (2)</b> - Upload & manage designs</summary>

<br>

| Tool | Description | Example Use |
|------|-------------|-------------|
| `printful_add_file` | Upload design file | "Upload my logo" |
| `printful_get_file` | Get file info & status | "Check file #12345" |

</details>

<details>
<summary><b>🏪 Store Tools (2)</b> - Manage stores & stats</summary>

<br>

| Tool | Description | Example Use |
|------|-------------|-------------|
| `printful_list_stores` | List your stores | "Show all my stores" |
| `printful_get_store_stats` | View sales & profit | "What are my sales?" |

</details>

<details>
<summary><b>🔄 Sync Product Tools (2)</b> - Legacy v1 features</summary>

<br>

| Tool | Description | Example Use |
|------|-------------|-------------|
| `printful_list_sync_products` | List synced products | "Show my Etsy products" |
| `printful_get_sync_product` | Get sync product details | "Details on sync #123" |

</details>

---

## 🎓 Documentation

<table>
<tr>
<td align="center" width="33%">

### 📖 [Quick Start Guide](QUICKSTART.md)
Get up and running in 5 minutes

</td>
<td align="center" width="33%">

### 🔑 [API Token Setup](API_TOKEN_SETUP.md)
Detailed token configuration guide

</td>
<td align="center" width="33%">

### 🧪 [Testing Guide](TESTING.md)
Learn how to test your integration

</td>
</tr>
<tr>
<td align="center" width="33%">

### 🔐 [API Scopes Reference](API_SCOPES_REFERENCE.md)
Required permissions explained

</td>
<td align="center" width="33%">

### 💻 [Examples](examples.py)
Real code examples

</td>
<td align="center" width="33%">

### 🔧 [Cursor Config](cursor-mcp-config.json)
Ready-to-use config file

</td>
</tr>
</table>

---

## 🔄 API Version Strategy

This server uses **Printful API v2** (production-ready beta) with smart **v1 fallback**:

<table>
<tr>
<td width="50%">

**🎯 v2 (Primary)**
- ✅ Catalog & Products
- ✅ Orders & Fulfillment
- ✅ Shipping Rates
- ✅ Mockup Generation
- ✅ File Management
- ✅ Store Statistics

</td>
<td width="50%">

**🔄 v1 (Fallback)**
- ✅ Sync Products
- ✅ Product Templates
- ⚠️ Auto-switches when needed
- 🚀 Future-proof architecture

</td>
</tr>
</table>

**Why v2?** Better pagination • Real-time stock • Enhanced orders • Improved security • Standardized formats

---

## ⚙️ Rate Limiting & Performance

<table>
<tr>
<td>

**📊 Rate Limits**
- 120 requests / 60 seconds
- Leaky bucket algorithm
- Auto-retry on 429 errors

</td>
<td>

**🚀 Performance**
- Response times: 100-500ms
- Concurrent requests: Supported
- Timeout handling: Built-in

</td>
</tr>
</table>

---

## 🐛 Troubleshooting

<details>
<summary><b>❌ "PRINTFUL_API_KEY environment variable is required"</b></summary>

<br>

**Solution:** Make sure your API key is set in `.env` or passed via environment variables in the MCP config.

```bash
# Check your .env file
cat .env

# Should contain:
PRINTFUL_API_KEY=your-actual-key-here
```

</details>

<details>
<summary><b>⏱️ "Rate limit exceeded"</b></summary>

<br>

**Solution:** Wait for the time specified in the error message (usually 60 seconds).

- Default limit: 120 requests/minute
- Consider implementing request batching
- Check `X-Ratelimit-Reset` header for exact reset time

</details>

<details>
<summary><b>🔍 "Resource not found"</b></summary>

<br>

**Solution:** Double-check the ID you're using.

- For orders: You can use external IDs by prefixing with `@` (e.g., `@my-order-123`)
- For products: Verify the product/variant ID exists in the catalog
- Check if the resource belongs to your store

</details>

<details>
<summary><b>🎨 Mockup generation stuck on "pending"</b></summary>

<br>

**Solution:** Mockup generation typically takes 10-30 seconds.

- Wait at least 30 seconds before checking status
- If stuck longer than 2 minutes, check task status - it may have failed
- Verify your design URL is publicly accessible

</details>

---

## 🧪 Testing

<div align="center">

### Choose Your Testing Method

</div>

<table>
<tr>
<td align="center" width="33%">

### ⚡ **Quick Test**
Automated test suite

```bash
export PRINTFUL_API_KEY=your-key
python test_server.py
```

✅ Tests 6 core features
⏱️ Takes 30 seconds

</td>
<td align="center" width="33%">

### 🌐 **Interactive Test**
Web-based MCP Inspector

```bash
export PRINTFUL_API_KEY=your-key
./test-with-inspector.sh
```

🎯 Test any tool visually
🌍 Opens at localhost:5173

</td>
<td align="center" width="33%">

### 🤖 **Live Test**
In Claude/Cursor

Just ask:

```
"List Printful countries"
```

💬 Natural language
✨ Real integration test

</td>
</tr>
</table>

**📖 Full testing guide:** See [TESTING.md](TESTING.md) for comprehensive testing instructions.

---

## 🏗️ Project Structure

```
printful-ph-mcp/
├── 📁 src/
│   └── 📁 printful_mcp/
│       ├── 🐍 server.py          # FastMCP server + tool registrations
│       ├── 🔌 client.py          # API client with auth/error handling
│       ├── 📁 tools/             # Tool implementations by domain
│       │   ├── 🛍️ catalog.py    # Product browsing (5 tools)
│       │   ├── 📦 orders.py     # Order management (4 tools)
│       │   ├── 🚚 shipping.py   # Shipping rates (2 tools)
│       │   ├── 🖼️ mockups.py    # Mockup generation (2 tools)
│       │   ├── 📁 files.py      # File management (2 tools)
│       │   ├── 🏪 stores.py     # Store statistics (2 tools)
│       │   └── 🔄 sync.py       # v1 fallback (2 tools)
│       └── 📁 models/
│           └── 📋 inputs.py      # Pydantic input models
├── 📄 pyproject.toml
├── 🔐 .env.example
└── 📖 README.md
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

<table>
<tr>
<td width="50%">

### 🐛 **Report Bugs**
Found an issue? [Open a bug report](https://github.com/Purple-Horizons/printful-ph-mcp/issues/new?labels=bug)

### ✨ **Request Features**
Have an idea? [Suggest a feature](https://github.com/Purple-Horizons/printful-ph-mcp/issues/new?labels=enhancement)

</td>
<td width="50%">

### 🔧 **Submit PRs**
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push and open a Pull Request

</td>
</tr>
</table>

---

## 📚 Resources & Links

<div align="center">

| Resource | Link |
|:--------:|:----:|
| 📘 **Printful API v2 Docs** | [developers.printful.com/docs/v2-beta](https://developers.printful.com/docs/v2-beta/) |
| 📗 **Printful API v1 Docs** | [developers.printful.com/docs](https://developers.printful.com/docs/) |
| 🔌 **MCP Protocol Spec** | [modelcontextprotocol.io](https://modelcontextprotocol.io/) |
| 🐍 **FastMCP Framework** | [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) |
| 🎨 **Purple Horizons** | [purplehorizons.io](https://purplehorizons.io) |
| 👨‍💻 **Made by Gianni** | [giannidalerta.com](https://giannidalerta.com) |

</div>

---

## 📄 License

<div align="center">

**MIT License** - Free to use, modify, and distribute

[View License](LICENSE) • [Purple Horizons LLC](https://purplehorizons.io) • 2026

</div>

---

## 💝 Support This Project

<div align="center">

### If this project helped you, consider:

⭐ **Star this repo** on GitHub

🐦 **Share it** on social media

🤝 **Contribute** to the codebase

🎨 **Sign up for Printful** using our affiliate link

<br>

<a href="https://www.printful.com/a/YOUR_AFFILIATE_ID">
  <img src="https://img.shields.io/badge/Try_Printful-Start_Free-FA4616?style=for-the-badge&logo=printful&logoColor=white" alt="Try Printful">
</a>

<br><br>

**Made with ❤️ by [Purple Horizons](https://purplehorizons.io)**

*Empowering businesses through AI automation*

</div>

---

<div align="center">

### 🚀 Ready to automate your print-on-demand business?

[**Get Started Now**](#installation) • [**View Examples**](#usage-examples) • [**Read Docs**](QUICKSTART.md)

<sub>Questions? Issues? [Open an issue](https://github.com/Purple-Horizons/printful-ph-mcp/issues) or [contact us](https://purplehorizons.io)</sub>

</div>
