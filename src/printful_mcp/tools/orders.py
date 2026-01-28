"""Order tools for Printful MCP server."""

import json
from typing import Dict, Any
from ..client import PrintfulClient, PrintfulAPIError
from ..models.inputs import (
    CreateOrderInput,
    GetOrderInput,
    ConfirmOrderInput,
    ListOrdersInput,
)


def format_order_markdown(order: Dict[str, Any]) -> str:
    """Format order data as markdown."""
    lines = [
        f"# Order {order['id']}",
        f"",
        f"**Status:** {order['status']}",
        f"**External ID:** {order.get('external_id', 'N/A')}",
        f"**Created:** {order['created_at']}",
        f"**Updated:** {order['updated_at']}",
        f"",
    ]
    
    # Recipient
    if order.get('recipient'):
        recipient = order['recipient']
        lines.extend([
            "## Recipient",
            f"**Name:** {recipient['name']}",
            f"**Address:** {recipient['address1']}",
            f"**City:** {recipient['city']}, {recipient.get('state_code', '')} {recipient['zip']}",
            f"**Country:** {recipient['country_name']} ({recipient['country_code']})",
            f"",
        ])
    
    # Costs
    if order.get('costs'):
        costs = order['costs']
        if costs['calculation_status'] == 'done':
            lines.extend([
                "## Costs",
                f"**Currency:** {costs['currency']}",
                f"**Subtotal:** {costs['subtotal']}",
                f"**Shipping:** {costs['shipping']}",
                f"**Tax:** {costs['tax']}",
                f"**Total:** {costs['total']}",
                f"",
            ])
        else:
            lines.extend([
                "## Costs",
                f"**Status:** {costs['calculation_status']}",
                f"",
            ])
    
    # Order items
    if order.get('order_items'):
        lines.append(f"## Order Items ({len(order['order_items'])})")
        for item in order['order_items']:
            lines.extend([
                f"- **Item {item['id']}**: {item.get('name', 'N/A')}",
                f"  - Variant: {item.get('catalog_variant_id', 'N/A')}",
                f"  - Quantity: {item['quantity']}",
                f"  - Price: {item.get('price', 'N/A')} {item.get('currency', '')}",
            ])
        lines.append("")
    
    return "\n".join(lines)


async def create_order(client: PrintfulClient, params: CreateOrderInput) -> str:
    """
    Create a new draft order.
    
    Creates an order in draft status. You'll need to add items separately using
    add_order_item, then confirm the order to start fulfillment.
    """
    try:
        order_data = {
            "recipient": {
                "name": params.recipient_name,
                "address1": params.recipient_address1,
                "city": params.recipient_city,
                "country_code": params.recipient_country_code,
                "zip": params.recipient_zip,
            }
        }
        
        if params.recipient_state_code:
            order_data["recipient"]["state_code"] = params.recipient_state_code
        if params.recipient_email:
            order_data["recipient"]["email"] = params.recipient_email
        if params.recipient_phone:
            order_data["recipient"]["phone"] = params.recipient_phone
        if params.external_id:
            order_data["external_id"] = params.external_id
        
        data = await client.post("/orders", json_data=order_data)
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            order = data.get('data', {})
            return format_order_markdown(order)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_order(client: PrintfulClient, params: GetOrderInput) -> str:
    """
    Get details of a specific order.
    
    Use order ID or external ID (prefix with @) to retrieve order information,
    including status, recipient, costs, and items.
    """
    try:
        data = await client.get(f"/orders/{params.order_id}")
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            order = data.get('data', {})
            return format_order_markdown(order)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def confirm_order(client: PrintfulClient, params: ConfirmOrderInput) -> str:
    """
    Confirm an order to start fulfillment.
    
    Moves order from draft to pending status and initiates production.
    Order must have items and costs calculated before confirmation.
    """
    try:
        data = await client.post(f"/orders/{params.order_id}/confirmation", json_data={})
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            order = data.get('data', {})
            return f"✓ Order {order['id']} confirmed successfully!\n\n" + format_order_markdown(order)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def list_orders(client: PrintfulClient, params: ListOrdersInput) -> str:
    """
    List all orders from the store.
    
    Returns a paginated list of orders with basic information.
    """
    try:
        query_params = {
            "limit": params.limit,
            "offset": params.offset,
        }
        
        data = await client.get("/orders", params=query_params)
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            orders = data.get('data', [])
            paging = data.get('paging', {})
            
            lines = [
                f"# Orders ({paging.get('total', 0)} total)",
                f"",
                f"Showing {len(orders)} orders (offset: {paging.get('offset', 0)}, limit: {paging.get('limit', 20)})",
                f"",
            ]
            
            for order in orders:
                costs = order.get('costs', {})
                total = costs.get('total', 'Calculating...')
                currency = costs.get('currency', '')
                
                lines.extend([
                    f"## Order {order['id']}",
                    f"- **Status:** {order['status']}",
                    f"- **External ID:** {order.get('external_id', 'N/A')}",
                    f"- **Total:** {total} {currency}",
                    f"- **Items:** {len(order.get('order_items', []))}",
                    f"- **Created:** {order['created_at']}",
                    f"",
                ])
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
