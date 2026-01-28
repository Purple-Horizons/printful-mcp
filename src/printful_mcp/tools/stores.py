"""Store tools for Printful MCP server."""

import json
from typing import Dict, Any
from ..client import PrintfulClient, PrintfulAPIError
from ..models.inputs import ListStoresInput, GetStoreStatsInput


async def list_stores(client: PrintfulClient, params: ListStoresInput) -> str:
    """
    List all stores available to the API token.
    
    Returns store IDs and names. Store-level tokens return one store,
    account-level tokens return all stores.
    """
    try:
        data = await client.get("/stores")
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            stores = data.get('data', [])
            
            lines = [
                f"# Stores ({len(stores)} total)",
                f"",
            ]
            
            for store in stores:
                lines.extend([
                    f"## {store['name']}",
                    f"- **ID:** {store['id']}",
                    f"- **Type:** {store['type']}",
                    f"",
                ])
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def get_store_statistics(client: PrintfulClient, params: GetStoreStatsInput) -> str:
    """
    Get store statistics for a date range.
    
    Returns sales, costs, profit, and other metrics. Available report types:
    - sales_and_costs: Detailed sales/costs by date
    - profit: Total profit in period
    - total_paid_orders: Number of paid orders
    - average_fulfillment_time: Avg fulfillment time
    """
    try:
        query_params = {
            "date_from": params.date_from,
            "date_to": params.date_to,
            "report_types": params.report_types,
        }
        
        if params.currency:
            query_params["currency"] = params.currency
        
        data = await client.get(f"/stores/{params.store_id}/statistics", params=query_params)
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            stats = data.get('data', {})
            currency = stats.get('currency', 'USD')
            
            lines = [
                f"# Store Statistics ({params.date_from} to {params.date_to})",
                f"",
                f"**Store ID:** {stats.get('store_id')}",
                f"**Currency:** {currency}",
                f"",
            ]
            
            # Profit
            if stats.get('profit'):
                profit = stats['profit']
                lines.extend([
                    "## Profit",
                    f"**Value:** {profit['value']} {currency}",
                    f"**Change:** {profit.get('relative_difference', 'N/A')}",
                    f"",
                ])
            
            # Total orders
            if stats.get('total_paid_orders'):
                orders = stats['total_paid_orders']
                lines.extend([
                    "## Total Paid Orders",
                    f"**Count:** {orders['value']}",
                    f"**Change:** {orders.get('relative_difference', 'N/A')}",
                    f"",
                ])
            
            # Printful costs
            if stats.get('printful_costs'):
                costs = stats['printful_costs']
                lines.extend([
                    "## Printful Costs",
                    f"**Value:** {costs['value']} {currency}",
                    f"**Change:** {costs.get('relative_difference', 'N/A')}",
                    f"",
                ])
            
            # Average fulfillment time
            if stats.get('average_fulfillment_time'):
                fulfill = stats['average_fulfillment_time']
                lines.extend([
                    "## Average Fulfillment Time",
                    f"**Days:** {fulfill['value']}",
                    f"**Change:** {fulfill.get('relative_difference', 'N/A')}",
                    f"",
                ])
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
