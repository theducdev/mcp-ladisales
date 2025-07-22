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
        Tạo mới chương trình khuyến mãi/mã giảm giá.
        
        Args:
            name (str): Tên chương trình khuyến mãi
            code (str): Mã khuyến mãi
            rule_type (int): Loại khuyến mãi (1: Mã khuyến mãi; 2: Chương trình khuyến mãi)
            type (Union[int, str]): Hình thức giảm giá (1: Theo %; 2: Theo số tiền)
            value (Union[float, str]): Giá trị giảm giá
            apply_to (Optional[Dict[str, int]]): Áp dụng với:
                - Toàn bộ sản phẩm: {"1": 1}
                - Tag sản phẩm: {"2": [product_tag_id1, product_tag_id2,...]} (Lấy từ API product-tag-search)
                - Sản phẩm cụ thể: {"3": [product_variant_id1, product_variant_id2,...]} (Lấy từ API product-variant-search)
            min_requirement (Optional[Dict[str, int]]): Yêu cầu tối thiểu:
                - Không yêu cầu: {"1": 1}
                - Tổng tiền tối thiểu: {"2": value} (value là giá trị tổng tiền tối thiểu)
                - Tổng số lượng sản phẩm tối thiểu: {"3": value}
            customer_groups (Optional[Dict[str, int]]): Nhóm khách hàng (Chỉ áp dụng với mã khuyến mãi):
                - Tất cả khách hàng: {"1": 1}
                - Tag khách hàng: {"2": [customer_tag_id1, customer_tag_id2,...]} (Lấy từ API customer-tag-search)
                - Khách hàng cụ thể: {"3": [customer_id1, customer_id2,...]} (Lấy từ API customer-search)
            usage_limit (Optional[int]): Giới hạn số lần sử dụng
            one_per_customer (int): Giới hạn mỗi khách hàng chỉ được sử dụng 1 lần (0: Không; 1: Có)
            start_date (Optional[str]): Ngày bắt đầu (định dạng ISO: YYYY-MM-DDTHH:mm:ss.sssZ)
            end_date (Optional[str]): Ngày kết thúc (định dạng ISO: YYYY-MM-DDTHH:mm:ss.sssZ)
            allow_promotion (int): Cho phép dùng chung với CTKM (0: Không; 1: Có)
        
        Returns:
            Dict: Thông tin chi tiết của discount sau khi tạo
            
        Example:
            create_discount(
                name="Khuyến mãi mùa xuân",
                code="SPRING",
                rule_type=1,
                type=2,
                value="10000",
                apply_to={"1": 1},
                min_requirement={"1": 1},
                customer_groups={"1": 1},
                usage_limit=None,
                one_per_customer=1,
                start_date="2024-01-12T07:55:28.814Z",
                allow_promotion=1
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
        Cập nhật thông tin chương trình khuyến mãi/mã giảm giá.
        
        Args:
            discount_id (Union[int, str]): ID của discount cần cập nhật
            name (Optional[str]): Tên chương trình khuyến mãi
            code (Optional[str]): Mã khuyến mãi
            rule_type (Optional[int]): Loại khuyến mãi (1: Mã khuyến mãi; 2: Chương trình khuyến mãi)
            type (Optional[Union[int, str]]): Hình thức giảm giá (1: Theo %; 2: Theo số tiền)
            value (Optional[Union[float, str]]): Giá trị giảm giá
            apply_to (Optional[Dict[str, int]]): Áp dụng với:
                - Toàn bộ sản phẩm: {"1": 1}
                - Tag sản phẩm: {"2": [product_tag_id1, product_tag_id2,...]} (Lấy từ API product-tag-search)
                - Sản phẩm cụ thể: {"3": [product_variant_id1, product_variant_id2,...]} (Lấy từ API product-variant-search)
            min_requirement (Optional[Dict[str, int]]): Yêu cầu tối thiểu:
                - Không yêu cầu: {"1": 1}
                - Tổng tiền tối thiểu: {"2": value} (value là giá trị tổng tiền tối thiểu)
                - Tổng số lượng sản phẩm tối thiểu: {"3": value}
            customer_groups (Optional[Dict[str, int]]): Nhóm khách hàng (Chỉ áp dụng với mã khuyến mãi):
                - Tất cả khách hàng: {"1": 1}
                - Tag khách hàng: {"2": [customer_tag_id1, customer_tag_id2,...]} (Lấy từ API customer-tag-search)
                - Khách hàng cụ thể: {"3": [customer_id1, customer_id2,...]} (Lấy từ API customer-search)
            usage_limit (Optional[int]): Giới hạn số lần sử dụng
            one_per_customer (Optional[int]): Giới hạn mỗi khách hàng chỉ được sử dụng 1 lần (0: Không; 1: Có)
            start_date (Optional[str]): Ngày bắt đầu (định dạng ISO: YYYY-MM-DDTHH:mm:ss.sssZ)
            end_date (Optional[str]): Ngày kết thúc (định dạng ISO: YYYY-MM-DDTHH:mm:ss.sssZ)
            allow_promotion (Optional[int]): Cho phép dùng chung với CTKM (0: Không; 1: Có)
        
        Returns:
            Dict: Thông tin chi tiết của discount sau khi cập nhật
            
        Example:
            update_discount(
                discount_id=44,
                name="Khuyến mãi mùa xuân",
                code="SPRING",
                rule_type=1,
                type=2,
                value="10000",
                apply_to={"1": 1},
                min_requirement={"1": 1},
                customer_groups={"1": 1},
                one_per_customer=1,
                start_date="2022-01-12T07:55:28.814Z",
                allow_promotion=1
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