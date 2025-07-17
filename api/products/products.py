"""
Product-related API tools for LaDiSales.
"""

from typing import Dict, List, Optional, Union
import requests
from mcp.server.fastmcp import FastMCP
from ..common.common import BASE_URL, headers, handle_api_response

def register_product_tools(mcp: FastMCP):
    """Register all product-related tools with the MCP server."""
    
    @mcp.tool()
    def list_products(page: int = 1, limit: int = 10) -> Dict:
        """
        Get a paginated list of all products.
        
        Args:
            page: Page number (default: 1)
            limit: Number of items per page (default: 10)
        
        Returns:
            Dict containing list of products
        """
        response = requests.post(
            f"{BASE_URL}/product/list",
            headers=headers,
            json={"page": page, "limit": limit}
        )
        return handle_api_response(response)

    @mcp.tool()
    def get_product(product_id: int) -> Dict:
        """
        Get detailed information about a specific product.
        
        Args:
            product_id: The unique identifier of the product
        
        Returns:
            Dict containing product details
        """
        response = requests.post(
            f"{BASE_URL}/product/show",
            headers=headers,
            json={"product_id": product_id}
        )
        return handle_api_response(response)

    @mcp.tool()
    def create_product(
        name: str,
        alias_name: str,
        description: str = "",
        inventory_checked: int = 0,
        type: str = "Physical",
        checkout_config_id: int = None,
        status: str = "Active",
        external_link: str = "",
        options: Optional[List[Dict]] = None,
        variants: Optional[List[Dict]] = None,
        tags: Optional[List[str]] = None,
        images: Optional[List[str]] = None,
        product_up_sells: Optional[List[int]] = None
    ) -> Dict:
        """
        Create a new product with specified parameters.
        
        Args:
            name: Product name (Required)
            alias_name: Product alias name (Required)
            description: Product description (Required)
            inventory_checked: Có quản lý kho hàng hay không (0: Không, 1: Có)
            type: Product type (default: "Physical")
            checkout_config_id: ID cấu hình thanh toán (Required)
            status: Product status (default: "Active")
            external_link: External link
            options: List of product options (size, color etc)
                Example:
                [
                    {
                        "name": "Kích cỡ",
                        "position": 1,
                        "type": 1,
                        "values": [
                            {"name": "M"},
                            {"name": "L"},
                            {"name": "S"}
                        ]
                    }
                ]
            variants: List of product variants
                Example:
                [
                    {
                        "options": {"Kích cỡ": "M"},
                        "price": "",
                        "price_compare": "",
                        "cost_per_item": "",
                        "weight": "",
                        "weight_unit": "g",
                        "sku": "",
                        "quantity": 0,
                        "src": "",
                        "position": 0
                    }
                ]
            tags: List of product tags
            images: List of product images
            product_up_sells: List of up-sell product IDs
        
        Returns:
            Dict containing the created product details including:
            - product_id: ID of created product
            - name: Product name
            - description: Product description
            - unit: Product unit
            - store_id: Store ID
            - created_at: Creation timestamp
            - is_delete: Deletion status
        """
        if options and not variants:
            raise ValueError("When providing options, variants must also be provided")

        data = {
            "product": {
                "name": name,
                "alias_name": alias_name,
                "description": description,
                "inventory_checked": inventory_checked,
                "type": type,
                "checkout_config_id": checkout_config_id,
                "status": status,
                "external_link": external_link,
                "tags": tags or [],
                "options": options or [],
                "variants": variants or [],
                "images": images or [],
                "product_up_sells": product_up_sells or []
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/product/create",
            headers=headers,
            json=data
        )
        return handle_api_response(response)

    @mcp.tool()
    def update_product(
        product_id: int,  # Required
        name: str,  # Required
        alias_name: str,  # Required
        domain: str = "",  # domain xuất bản
        path: str = "",  # đường dẫn xuất bản
        payment_redirect_url: str = "",  # Đường dẫn chuyển trang
        payment_redirect_after: int = 5,  # Chuyển trang sau bao lâu
        description: str = "",  # Mô tả
        price: Union[float, str] = "",  # giá
        price_compare: Union[float, str] = "",  # giá so sánh
        cost_per_item: Union[float, str] = "",  # giá vốn
        sku: str = "",  # Mã SKU
        weight: Union[float, str] = "",  # Khối lượng
        weight_unit: str = "",  # Đơn vị khối lượng (g, kg)
        inventory_checked: Union[int, str] = "",  # Có quản lý tồn kho hay không
        quantity: Union[int, str] = "",  # Số lượng tồn kho
        type: str = "Physical",  # loại sản phẩm
        checkout_config_id: int = None,  # id của trang thanh toán
        status: str = "Active",  # Ẩn hoặc hiển thị sản phẩm với bên ngoài
        external_link: str = "",  # Đường dẫn external
        variants: Optional[List[Dict]] = None,  # Danh sách biến thể
        tags: Optional[List] = None,  # Danh sách tags
        product_up_sells: Optional[List] = None,  # Danh sách sản phẩm up-sell
        is_publish: bool = True  # Trạng thái xuất bản
    ) -> Dict:
        """
        Update an existing product.
        
        Args:
            product_id: ID sản phẩm (Required)
            name: Tên sản phẩm (Required)
            alias_name: Tên alias (Required)
            domain: Domain xuất bản (default: "")
            path: Đường dẫn xuất bản (default: "")
            payment_redirect_url: Đường dẫn chuyển trang (default: "")
            payment_redirect_after: Chuyển trang sau bao lâu (giây) (default: 5)
            description: Mô tả sản phẩm (default: "")
            price: Giá bán (default: "")
            price_compare: Giá so sánh (default: "")
            cost_per_item: Giá vốn (default: "")
            sku: Mã SKU (default: "")
            weight: Khối lượng (default: "")
            weight_unit: Đơn vị khối lượng (g, kg) (default: "")
            inventory_checked: Có quản lý tồn kho hay không (default: "")
            quantity: Số lượng tồn kho (default: "")
            type: Loại sản phẩm (default: "Physical")
            checkout_config_id: ID trang thanh toán
            status: Trạng thái hiển thị (default: "Active")
            external_link: Đường dẫn external (default: "")
            variants: Danh sách biến thể sản phẩm
                Example:
                [
                    {
                        "product_variant_id": 2048,  # ID biến thể
                        "price": 0,
                        "price_compare": null,
                        "cost_per_item": 0,
                        "sku": "",
                        "quantity": 0,
                        "package_price": 0,  # Giá trung bình với sản phẩm dịch vụ
                        "package_quantity_unit": null,  # Đơn vị tính cho dịch vụ
                        "package_quantity": 0,  # Số lượng cho dịch vụ
                        "package_addition_quantity": 0,  # Số lượng cộng thêm cho dịch vụ
                        "inventory_checked": 0,
                        "weight": 0,
                        "weight_unit": "g",
                        "src": "",
                        "start_date": null,
                        "end_date": null,
                        "timezone": "Asia/Bangkok",
                        "max_buy": null,
                        "min_buy": null,
                        "total_sold": 0,
                        "total_quantity": null,
                        "description": null,
                        "position": 0,
                        "status": null,
                        "name": "product-name-M",
                        "title": "M",
                        "options": [
                            {
                                "variant_value_id": "3922",  # ID của biến thể + option + option_value
                                "option_id": "456",  # ID của option
                                "option_name": "Kích cỡ",
                                "option_value_id": "1505",  # ID của giá trị trong option
                                "option_value_value": {
                                    "name": "M"
                                }
                            }
                        ]
                    }
                ]
            tags: Danh sách tags (default: [])
            product_up_sells: Danh sách ID sản phẩm up-sell (default: [])
            is_publish: Trạng thái xuất bản (default: true)
        
        Returns:
            Dict containing the updated product details
        """
        data = {
            "product": {
                "product_id": product_id,
                "name": name,
                "alias_name": alias_name,
                "domain": domain,
                "path": path,
                "payment_redirect_url": payment_redirect_url,
                "payment_redirect_after": payment_redirect_after,
                "description": description,
                "price": price,
                "price_compare": price_compare,
                "cost_per_item": cost_per_item,
                "sku": sku,
                "weight": weight,
                "weight_unit": weight_unit,
                "inventory_checked": inventory_checked,
                "quantity": quantity,
                "type": type,
                "checkout_config_id": checkout_config_id,
                "status": status,
                "external_link": external_link,
                "variants": variants or [],
                "tags": tags or [],
                "product_up_sells": product_up_sells or [],
                "is_publish": is_publish
            }
        }
        
        # Remove None values
        data["product"] = {k: v for k, v in data["product"].items() if v is not None}
        
        response = requests.post(
            f"{BASE_URL}/product/update",
            headers=headers,
            json=data
        )
        return handle_api_response(response)

    @mcp.tool()
    def delete_product(product_id: int) -> Dict:
        """
        Delete a product.
        
        Args:
            product_id: The unique identifier of the product to delete
        
        Returns:
            Dict containing the deletion confirmation
        """
        response = requests.post(
            f"{BASE_URL}/product/delete",
            headers=headers,
            json={"product_id": product_id}
        )
        return handle_api_response(response)

    @mcp.tool()
    def list_checkout_configs() -> Dict:
        """
        Get list of available checkout configurations.
        
        Returns:
            Dict containing list of checkout configurations
        """
        response = requests.post(
            f"{BASE_URL}/checkout-config/list",
            headers=headers
        )
        return handle_api_response(response) 