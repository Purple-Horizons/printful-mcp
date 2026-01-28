"""Shipping tools for Printful MCP server."""

import json
from typing import Dict, Any
from ..client import PrintfulClient, PrintfulAPIError
from ..models.inputs import CalculateShippingInput


async def calculate_shipping_rates(client: PrintfulClient, params: CalculateShippingInput) -> str:
    """
    Calculate shipping rates for an order.
    
    Provides available shipping methods and costs based on recipient location
    and order items. Returns estimated delivery times and customs fee information.
    """
    try:
        # Parse items JSON
        try:
            items = json.loads(params.items_json)
        except json.JSONDecodeError:
            return "Error: items_json must be valid JSON array. Example: [{\"catalog_variant_id\": 4011, \"quantity\": 1, \"source\": \"catalog\", \"placements\": [...]}]"
        
        request_data = {
            "recipient": {
                "country_code": params.recipient_country_code,
            },
            "order_items": items,
        }
        
        if params.recipient_state_code:
            request_data["recipient"]["state_code"] = params.recipient_state_code
        if params.recipient_city:
            request_data["recipient"]["city"] = params.recipient_city
        if params.recipient_zip:
            request_data["recipient"]["zip"] = params.recipient_zip
        if params.currency:
            request_data["currency"] = params.currency
        
        data = await client.post("/shipping-rates", json_data=request_data)
        
        if params.format == "json":
            return json.dumps(data, indent=2)
        else:
            rates = data.get('data', [])
            
            lines = [
                f"# Shipping Rates",
                f"",
                f"Found {len(rates)} shipping options",
                f"",
            ]
            
            for rate in rates:
                delivery = f"{rate['min_delivery_days']}-{rate['max_delivery_days']} days"
                lines.extend([
                    f"## {rate['shipping_method_name']}",
                    f"- **Rate:** {rate['rate']} {rate['currency']}",
                    f"- **Delivery:** {delivery} ({rate['min_delivery_date']} to {rate['max_delivery_date']})",
                    f"",
                ])
                
                if rate.get('shipments'):
                    lines.append("### Shipments")
                    for shipment in rate['shipments']:
                        customs = "Yes" if shipment.get('customs_fees_possible') else "No"
                        lines.append(f"- From {shipment['departure_country']} - Customs fees possible: {customs}")
                    lines.append("")
            
            return "\n".join(lines)
            
    except PrintfulAPIError as e:
        return f"Error: {e.message}"


async def list_countries(client: PrintfulClient) -> str:
    """
    List all countries where Printful is available.
    
    Returns country codes and state codes needed for order creation.
    Useful for address validation and form building.
    """
    try:
        data = await client.get("/countries", params={"limit": 250})
        
        countries = data.get('data', [])
        
        lines = [
            f"# Available Countries ({len(countries)} total)",
            f"",
        ]
        
        for country in countries:
            lines.append(f"## {country['name']} ({country['code']})")
            
            if country.get('states'):
                lines.append(f"**States:** {len(country['states'])} available")
                # Show first few states
                for state in country['states'][:3]:
                    lines.append(f"  - {state['name']} ({state['code']})")
                if len(country['states']) > 3:
                    lines.append(f"  - _(and {len(country['states']) - 3} more)_")
            lines.append("")
        
        return "\n".join(lines)
        
    except PrintfulAPIError as e:
        return f"Error: {e.message}"
