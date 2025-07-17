"""
Discount-related API tools for LaDiSales.
"""

from typing import Dict, Optional, Union, List
import requests
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from ..common.common import BASE_URL, headers, handle_api_response

# Constants for discount types
DISCOUNT_TYPE_FIXED = 1
DISCOUNT_TYPE_PERCENTAGE = 2

def register_discount_tools(mcp: FastMCP):
    """Register all discount-related tools with the MCP server."""

    @mcp.tool()
    def search_product_tags(search: str = "") -> Dict:
        """
        Search product tags.
        
        Args:
            search: Search keyword (empty string returns all tags)
        
        Returns:
            Dict containing search results
        """
        response = requests.post(
            f"{BASE_URL}/product-tag/search",
            headers=headers,
            json={"search": search},
            verify=False
        )
        return handle_api_response(response)

    @mcp.tool()
    def search_product_variants(search: str = "") -> Dict:
        """
        Search product variants.
        
        Args:
            search: Search keyword (empty string returns all variants)
        
        Returns:
            Dict containing search results
        """
        response = requests.post(
            f"{BASE_URL}/product-variant/search",
            headers=headers,
            json={"search": search},
            verify=False
        )
        return handle_api_response(response)

    @mcp.tool()
    def search_customer_tags(search: str = "") -> Dict:
        """
        Search customer tags.
        
        Args:
            search: Search keyword (empty string returns all tags)
        
        Returns:
            Dict containing search results
        """
        response = requests.post(
            f"{BASE_URL}/customer-tag/search",
            headers=headers,
            json={"search": search},
            verify=False
        )
        return handle_api_response(response)

    @mcp.tool()
    def search_customers(search: str = "") -> Dict:
        """
        Search customers.
        
        Args:
            search: Search keyword (empty string returns all customers)
        
        Returns:
            Dict containing search results
        """
        response = requests.post(
            f"{BASE_URL}/customer/search",
            headers=headers,
            json={"search": search},
            verify=False
        )
        return handle_api_response(response)
    
    @mcp.tool()
    def create_discount(
        name: str,
        code: str,
        type: Union[int, str],
        value: Union[float, str],
        apply_to: Optional[Dict[str, int]] = None,
        min_requirement: Optional[Dict[str, int]] = None,
        customer_groups: Optional[Dict[str, int]] = None,
        usage_limit: Optional[int] = None,
        one_per_customer: int = 1,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        rule_type: int = 1,
        allow_promotion: int = 1
    ) -> Dict:
        """
        Create a new discount.
        
        Args:
            name: Discount name
            code: Unique discount code (alphanumeric)
            type: Discount type:
                - 1: Fixed amount
                - 2: Percentage
                Can be passed as int or string ("fixed"/"percentage")
            value: Discount value (as string)
            apply_to: Dict of application rules
                Example: {"1": 1} for all products
            min_requirement: Dict of minimum requirements
                Example: {"1": 1} for all orders
            customer_groups: Dict of customer group rules
                Example: {"1": 1} for all customers
            usage_limit: Maximum number of uses (null for unlimited)
            one_per_customer: Whether each customer can use only once (1) or multiple times (0)
            start_date: Start date (ISO format)
            end_date: End date (ISO format, null for no end date)
            rule_type: Type of discount rule (default: 1)
            allow_promotion: Whether discount can be combined (1) or not (0)
        
        Returns:
            Dict containing the created discount details
            
        Example:
            create_discount(
                name="Spring Sale",
                code="SPRING",
                type=2,
                value="10000",
                apply_to={"1": 1},
                min_requirement={"1": 1},
                customer_groups={"1": 1},
                usage_limit=None,
                one_per_customer=1,
                start_date="2024-01-12T07:55:28.814Z"
            )
        """
        # Convert string type to number if needed
        if isinstance(type, str):
            type = DISCOUNT_TYPE_PERCENTAGE if type.lower() == "percentage" else DISCOUNT_TYPE_FIXED
            
        # Set default values
        if apply_to is None:
            apply_to = {"1": 1}
        if min_requirement is None:
            min_requirement = {"1": 1}
        if customer_groups is None:
            customer_groups = {"1": 1}
            
        data = {
            "discount": {
                "name": name,
                "code": code,
                "type": type,
                "value": str(value),
                "apply_to": apply_to,
                "min_requirement": min_requirement,
                "customer_groups": customer_groups,
                "usage_limit": usage_limit,
                "one_per_customer": one_per_customer,
                "start_date": start_date,
                "end_date": end_date,
                "rule_type": rule_type,
                "allow_promotion": allow_promotion
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/discount/create",
            headers=headers,
            json=data,
            verify=False
        )
        return handle_api_response(response)

    @mcp.tool()
    def update_discount(
        discount_id: Union[int, str],
        name: Optional[str] = None,
        code: Optional[str] = None,
        type: Optional[Union[int, str]] = None,
        value: Optional[Union[float, str]] = None,
        apply_to: Optional[Dict[str, int]] = None,
        min_requirement: Optional[Dict[str, int]] = None,
        customer_groups: Optional[Dict[str, int]] = None,
        usage_limit: Optional[int] = None,
        one_per_customer: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        rule_type: Optional[int] = None,
        allow_promotion: Optional[int] = None
    ) -> Dict:
        """
        Update an existing discount.
        
        Args:
            discount_id: ID of the discount to update
            Other parameters: Same as create_discount, all optional
        
        Returns:
            Dict containing the updated discount details
            
        Example:
            update_discount(
                discount_id=44,
                code="SPRING",
                value="10000",
                type=2
            )
        """
        # Convert string type to number if needed
        if isinstance(type, str):
            type = DISCOUNT_TYPE_PERCENTAGE if type.lower() == "percentage" else DISCOUNT_TYPE_FIXED
            
        # Build update data with only provided fields
        update_data = {
            "discount_id": discount_id
        }
        
        if name is not None:
            update_data["name"] = name
        if code is not None:
            update_data["code"] = code
        if type is not None:
            update_data["type"] = type
        if value is not None:
            update_data["value"] = str(value)
        if apply_to is not None:
            update_data["apply_to"] = apply_to
        if min_requirement is not None:
            update_data["min_requirement"] = min_requirement
        if customer_groups is not None:
            update_data["customer_groups"] = customer_groups
        if usage_limit is not None:
            update_data["usage_limit"] = usage_limit
        if one_per_customer is not None:
            update_data["one_per_customer"] = one_per_customer
        if start_date is not None:
            update_data["start_date"] = start_date
        if end_date is not None:
            update_data["end_date"] = end_date
        if rule_type is not None:
            update_data["rule_type"] = rule_type
        if allow_promotion is not None:
            update_data["allow_promotion"] = allow_promotion
        
        data = {
            "discount": update_data
        }
        
        response = requests.post(
            f"{BASE_URL}/discount/update",
            headers=headers,
            json=data,
            verify=False
        )
        return handle_api_response(response)

    @mcp.tool()
    def delete_discount(discount_id: Union[int, str]) -> Dict:
        """
        Delete a discount.
        
        Args:
            discount_id: ID of the discount to delete
        
        Returns:
            Dict containing the deletion confirmation
            
        Example:
            delete_discount(44)
        """
        response = requests.post(
            f"{BASE_URL}/discount/delete",
            headers=headers,
            json={"discount_id": discount_id},
            verify=False
        )
        return handle_api_response(response) 