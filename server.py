"""
FastMCP server for LaDiSales API integration with streamable-http support.

This module provides tools for interacting with the LaDiSales API, including:
- Discount management (create, update, delete, list, search)
- Product management (create, update, delete, list, search, categories)
- Customer management (create, update, delete, list, search, groups)
- Location management (country, state, district, ward lists)
"""

from mcp.server.fastmcp import FastMCP
from api.discounts.discounts import register_discount_tools
from api.products.products import register_product_tools
from api.customers.customers import register_customer_tools
from api.location.location import register_location_tools

# Create an MCP server
mcp = FastMCP("LaDiSales")

# Register all tools
register_discount_tools(mcp)
register_product_tools(mcp)
register_customer_tools(mcp)
register_location_tools(mcp)