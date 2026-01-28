"""Mockup generator tools for Printful MCP server."""

import json
from typing import Dict, Any
from ..client import PrintfulClient, PrintfulAPIError
from ..models.inputs import CreateMockupTaskInput, GetMockupTaskInput


async def create_mockup_task(client: PrintfulClient, params: CreateMockupTaskInput) -> str:
    """
    Create a mockup generation task.
    
    Generates product mockups asynchronously. Returns a task ID that can be used
    to check status and retrieve mockup URLs. Process typically takes 10-30 seconds.
    """
    try:
        # Parse comma-separated IDs
        variant_ids = [int(v.strip()) for v in params.variant_ids.split(",")]
        style_ids = [int(s.strip()) for s in params.mockup_style_ids.split(",")]
        
        request_data = {
            "format": params.format,
            "products": [{
                "source": "catalog",
                "catalog_product_id": params.product_id,
                "catalog_variant_ids": variant_ids,
                "mockup_style_ids": style_ids,
                "placements": [{
                    "placement": params.placement,
                    "technique": params.technique,
                    "layers": [{
                        "type": "file",
                        "url": params.design_url,
                    }]
                }]
            }]
        }
        
        data = await client.post("/mockup-tasks", json_data=request_data)
        
        # Return the task info
        tasks = data.get('data', [])
        if tasks:
            task = tasks[0]
            return f"Mockup task created!\n\nTask ID: {task['id']}\nStatus: {task['status']}\n\nUse printful_get_mockup_task with this ID to check status and get mockup URLs."
        else:
            return json.dumps(data, indent=2)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
    except (ValueError, KeyError) as e:
        return f"Error parsing input: {str(e)}"


async def get_mockup_task(client: PrintfulClient, params: GetMockupTaskInput) -> str:
    """
    Get mockup task status and results.
    
    Check if mockup generation is complete and retrieve mockup image URLs.
    Task status can be: pending, completed, or failed.
    """
    try:
        data = await client.get("/mockup-tasks", params={"id": params.task_id})
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            tasks = data.get('data', [])
            if not tasks:
                return f"No task found with ID {params.task_id}"
            
            task = tasks[0]
            lines = [
                f"# Mockup Task {task['id']}",
                f"",
                f"**Status:** {task['status']}",
                f"",
            ]
            
            if task['status'] == 'completed':
                variant_mockups = task.get('catalog_variant_mockups', [])
                lines.append(f"## Generated Mockups ({len(variant_mockups)} variants)")
                
                for vm in variant_mockups:
                    lines.append(f"### Variant {vm['catalog_variant_id']}")
                    for mockup in vm.get('mockups', []):
                        lines.extend([
                            f"- **{mockup['display_name']}** ({mockup['placement']})",
                            f"  - Style ID: {mockup['style_id']}",
                            f"  - URL: {mockup['mockup_url']}",
                        ])
                    lines.append("")
            
            elif task['status'] == 'pending':
                lines.append("⏳ Mockup generation in progress. Check again in a few seconds.")
            
            elif task['status'] == 'failed':
                lines.append("❌ Mockup generation failed.")
                if task.get('failure_reasons'):
                    lines.append("\n**Reasons:**")
                    for reason in task['failure_reasons']:
                        lines.append(f"- {reason.get('detail', 'Unknown error')}")
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
