"""Pydantic input models for Printful MCP tools."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class ResponseFormat(BaseModel):
    """Response format preference."""
    format: Literal["markdown", "json"] = Field(
        default="markdown",
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


# Catalog Models
class ListCatalogProductsInput(BaseModel):
    """Input for listing catalog products."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Number of results per page")
    offset: Optional[int] = Field(default=0, ge=0, description="Number of results to skip")
    category_ids: Optional[str] = Field(default=None, description="Comma-separated category IDs")
    colors: Optional[str] = Field(default=None, description="Comma-separated color names")
    techniques: Optional[str] = Field(default=None, description="Comma-separated techniques (dtg, embroidery, etc.)")
    types: Optional[str] = Field(default=None, description="Comma-separated product types")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetProductInput(BaseModel):
    """Input for getting a single product."""
    product_id: int = Field(..., description="Catalog product ID")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetProductVariantsInput(BaseModel):
    """Input for getting product variants."""
    product_id: int = Field(..., description="Catalog product ID")
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Number of results per page")
    offset: Optional[int] = Field(default=0, ge=0, description="Number of results to skip")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetVariantPricesInput(BaseModel):
    """Input for getting variant prices."""
    variant_id: int = Field(..., description="Catalog variant ID")
    currency: Optional[str] = Field(default=None, description="Currency code (e.g., USD, EUR)")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetProductAvailabilityInput(BaseModel):
    """Input for getting product availability."""
    product_id: int = Field(..., description="Catalog product ID")
    techniques: Optional[str] = Field(default=None, description="Comma-separated techniques to filter")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


# Order Models
class CreateOrderInput(BaseModel):
    """Input for creating an order."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    recipient_name: str = Field(..., description="Recipient name")
    recipient_address1: str = Field(..., description="Recipient address line 1")
    recipient_city: str = Field(..., description="Recipient city")
    recipient_country_code: str = Field(..., description="Recipient country code (e.g., US)")
    recipient_zip: str = Field(..., description="Recipient ZIP/postal code")
    recipient_state_code: Optional[str] = Field(default=None, description="State code (required for US, CA, AU)")
    recipient_email: Optional[str] = Field(default=None, description="Recipient email")
    recipient_phone: Optional[str] = Field(default=None, description="Recipient phone")
    external_id: Optional[str] = Field(default=None, description="Your order ID for reference")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetOrderInput(BaseModel):
    """Input for getting an order."""
    order_id: str = Field(..., description="Order ID or external ID (prefix with @ for external ID)")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class ConfirmOrderInput(BaseModel):
    """Input for confirming an order."""
    order_id: str = Field(..., description="Order ID or external ID (prefix with @ for external ID)")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class ListOrdersInput(BaseModel):
    """Input for listing orders."""
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Number of results per page")
    offset: Optional[int] = Field(default=0, ge=0, description="Number of results to skip")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


# Shipping Models
class CalculateShippingInput(BaseModel):
    """Input for calculating shipping rates."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    recipient_country_code: str = Field(..., description="Recipient country code (e.g., US)")
    recipient_state_code: Optional[str] = Field(default=None, description="State code (required for US, CA, AU)")
    recipient_city: Optional[str] = Field(default=None, description="Recipient city")
    recipient_zip: Optional[str] = Field(default=None, description="Recipient ZIP/postal code")
    items_json: str = Field(..., description="JSON array of order items with catalog_variant_id and quantity")
    currency: Optional[str] = Field(default=None, description="Currency code (e.g., USD)")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


# Mockup Models
class CreateMockupTaskInput(BaseModel):
    """Input for creating a mockup generation task."""
    product_id: int = Field(..., description="Catalog product ID")
    variant_ids: str = Field(..., description="Comma-separated variant IDs")
    mockup_style_ids: str = Field(..., description="Comma-separated mockup style IDs")
    design_url: str = Field(..., description="URL to design image file")
    placement: str = Field(default="front", description="Placement (e.g., front, back)")
    technique: str = Field(default="dtg", description="Technique (e.g., dtg, embroidery)")
    format: Literal["jpg", "png"] = Field(default="jpg", description="Output image format")


class GetMockupTaskInput(BaseModel):
    """Input for getting mockup task status."""
    task_id: str = Field(..., description="Mockup task ID")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


# File Models
class AddFileInput(BaseModel):
    """Input for adding a file to library."""
    url: str = Field(..., description="URL to the file to add")
    filename: Optional[str] = Field(default=None, description="Custom filename")
    visible: bool = Field(default=True, description="Show in file library")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetFileInput(BaseModel):
    """Input for getting file info."""
    file_id: int = Field(..., description="File ID")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


# Store Models
class ListStoresInput(BaseModel):
    """Input for listing stores."""
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")


class GetStoreStatsInput(BaseModel):
    """Input for getting store statistics."""
    store_id: int = Field(..., description="Store ID")
    date_from: str = Field(..., description="Start date (YYYY-MM-DD)")
    date_to: str = Field(..., description="End date (YYYY-MM-DD)")
    report_types: str = Field(
        default="sales_and_costs,profit",
        description="Comma-separated report types (e.g., sales_and_costs,profit,total_paid_orders)"
    )
    currency: Optional[str] = Field(default=None, description="Currency code")
    format: Literal["markdown", "json"] = Field(default="markdown", description="Output format")
