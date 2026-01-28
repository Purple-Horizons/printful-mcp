# Printful MCP Cursor Skill

This directory contains a Cursor AI skill that teaches AI assistants how to effectively use the Printful MCP server.

## What is this?

A single skill file (`printful-mcp/SKILL.md`) that provides:
- Instructions for all 17 Printful MCP tools
- Common workflows (product discovery, orders, mockups, shipping)
- Best practices and troubleshooting
- Output formatting guidelines

## How it works

When you open this project in Cursor and ask Printful-related questions, the AI automatically:
1. Detects Printful/print-on-demand keywords
2. Applies the skill's guidance
3. Uses the appropriate MCP tools
4. Follows best practices
5. Formats results clearly

## Installation

**For this project:** Already included! Just open in Cursor and start asking questions.

**For personal use across all projects:**
```bash
cp -r .cursor/skills/printful-mcp ~/.cursor/skills/
```

## Usage Examples

Just ask naturally:
- "Show me all t-shirts under $15"
- "Create an order for John Doe in Los Angeles"
- "Generate a mockup with my design"
- "Calculate shipping to UK"
- "What are my store statistics?"

The skill ensures the AI knows how to use each tool correctly and follows proper workflows.

## File Structure

```
.cursor/skills/
└── printful-mcp/
    └── SKILL.md    (Single skill file)
```

That's it! One skill, professionally crafted, ready to use.
