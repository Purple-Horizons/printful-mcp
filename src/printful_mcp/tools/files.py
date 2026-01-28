"""File library tools for Printful MCP server."""

import json
from typing import Dict, Any
from ..client import PrintfulClient, PrintfulAPIError
from ..models.inputs import AddFileInput, GetFileInput


async def add_file(client: PrintfulClient, params: AddFileInput) -> str:
    """
    Add a file to the Printful file library.
    
    Uploads a design file from URL. The file is processed asynchronously.
    Status will be 'waiting' initially, then 'ok' or 'failed' after processing.
    """
    try:
        request_data = {
            "url": params.url,
            "visible": params.visible,
        }
        
        if params.filename:
            request_data["filename"] = params.filename
        
        data = await client.post("/files", json_data=request_data)
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            file_data = data.get('data', {})
            
            lines = [
                f"# File Added to Library",
                f"",
                f"**File ID:** {file_data['id']}",
                f"**Status:** {file_data['status']}",
                f"**Filename:** {file_data.get('filename', 'Pending')}",
                f"**Original URL:** {file_data['url']}",
                f"",
            ]
            
            if file_data['status'] == 'ok':
                lines.extend([
                    f"**Dimensions:** {file_data.get('width')}x{file_data.get('height')}px",
                    f"**DPI:** {file_data.get('dpi')}",
                    f"**Size:** {file_data.get('size')} bytes",
                    f"**Preview:** {file_data.get('preview_url')}",
                    f"",
                ])
            elif file_data['status'] == 'waiting':
                lines.append("⏳ File is being processed. Check status with printful_get_file.")
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_file(client: PrintfulClient, params: GetFileInput) -> str:
    """
    Get information about a file in the library.
    
    Returns file details including processing status, dimensions, and URLs.
    """
    try:
        data = await client.get(f"/files/{params.file_id}")
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            file_data = data.get('data', {})
            
            lines = [
                f"# File {file_data['id']}",
                f"",
                f"**Status:** {file_data['status']}",
                f"**Filename:** {file_data.get('filename', 'N/A')}",
                f"**MIME Type:** {file_data.get('mime_type', 'N/A')}",
                f"**Created:** {file_data['created']}",
                f"",
            ]
            
            if file_data['status'] == 'ok':
                lines.extend([
                    "## File Details",
                    f"- **Dimensions:** {file_data.get('width')}x{file_data.get('height')}px",
                    f"- **DPI:** {file_data.get('dpi')}",
                    f"- **Size:** {file_data.get('size')} bytes",
                    f"- **Hash:** {file_data.get('hash')}",
                    f"",
                    "## URLs",
                    f"- **Original:** {file_data['url']}",
                    f"- **Thumbnail:** {file_data.get('thumbnail_url')}",
                    f"- **Preview:** {file_data.get('preview_url')}",
                    f"",
                ])
            elif file_data['status'] == 'waiting':
                lines.append("⏳ File is still being processed.")
            elif file_data['status'] == 'failed':
                lines.append("❌ File processing failed. The file may be invalid or inaccessible.")
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
