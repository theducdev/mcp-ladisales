"""
Customer-related API tools for LaDiSales.
"""

from typing import Dict, List, Optional, Any
import requests
from mcp.server.fastmcp import FastMCP
from ..common.common import BASE_URL, headers, handle_api_response

def register_customer_tools(mcp: FastMCP):
    """Register all customer-related tools with the MCP server."""
    
    @mcp.tool()
    def get_customer(customer_id: str) -> Dict:
        """
        Lấy thông tin chi tiết của một khách hàng cụ thể.
        
        Args:
            customer_id: ID của khách hàng cần lấy thông tin
        
        Returns:
            Dict chứa thông tin chi tiết của khách hàng bao gồm:
            - customer_id: ID khách hàng
            - first_name: Tên
            - last_name: Họ
            - email: Địa chỉ email
            - phone: Số điện thoại
            - note: Ghi chú
            - tags: Danh sách tag
            - custom_fields: Danh sách các trường tùy chỉnh
            
        Example:
            get_customer("989898940")
        """
        data = {
            "customer_id": customer_id
        }
        
        response = requests.post(
            f"{BASE_URL}/customer/show",
            headers=headers,
            json=data
        )
        return handle_api_response(response)

    @mcp.tool()
    def create_customer(
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        note: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[List[Dict]] = None,
        address: Optional[Dict] = None,
        ref_type: str = "ls"
    ) -> Dict:
        """
        Tạo một khách hàng mới.
        
        Args:
            first_name: Tên của khách hàng
            last_name: Họ của khách hàng
            email: Địa chỉ email (phải là duy nhất)
            phone: Số điện thoại (phải là duy nhất)
            note: Ghi chú về khách hàng (tùy chọn)
            tags: Danh sách các tag (tùy chọn)
            custom_fields: Danh sách các trường tùy chỉnh (tùy chọn)
                Mỗi trường có dạng:
                {
                    "custom_field_id": int,
                    "value": str
                }
            address: Thông tin địa chỉ (tùy chọn)
                {
                    "first_name": str,
                    "last_name": str,
                    "company": str,
                    "address": str,
                    "apartment": str,
                    "country_code": str,
                    "country_name": str,
                    "postal_code": str,
                    "state_id": int,
                    "state_name": str,
                    "district_id": int,
                    "district_name": str,
                    "ward_id": int,
                    "ward_name": str,
                    "phone": str
                }
            ref_type: Loại tham chiếu (mặc định: "ls")
        
        Returns:
            Dict chứa thông tin khách hàng đã tạo
            
        Example:
            create_customer(
                first_name="Chu",
                last_name="Manh",
                email="example@gmail.com",
                phone="0983333222",
                note="Ghi chu",
                tags=["Tag"],
                custom_fields=[
                    {
                        "custom_field_id": 27,
                        "value": ""
                    }
                ],
                address={
                    "first_name": "Chu",
                    "last_name": "Manh",
                    "address": "Dia chi",
                    "apartment": "Dia chi 2",
                    "country_code": "VN",
                    "country_name": "Việt Nam",
                    "postal_code": "1000",
                    "state_id": 201,
                    "state_name": "Hà Nội",
                    "district_id": 1482,
                    "district_name": "Quận Bắc Từ Liêm",
                    "ward_id": 1642,
                    "ward_name": "Phường Liên Mạc",
                    "phone": "0943555666"
                }
            )
        """
        data = {
            "customer": {
                "ref_type": ref_type,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "note": note,
                "tags": tags or [],
                "custom_fields": custom_fields or [],
                "address": address or {}
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/customer/create",
            headers=headers,
            json=data
        )
        return handle_api_response(response)

    @mcp.tool()
    def update_customer(
        customer_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        note: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Cập nhật thông tin của một khách hàng.
        
        Args:
            customer_id: ID của khách hàng cần cập nhật
            first_name: Tên mới của khách hàng
            last_name: Họ mới của khách hàng
            email: Địa chỉ email mới (phải là duy nhất)
            phone: Số điện thoại mới (phải là duy nhất)
            note: Ghi chú mới về khách hàng
            tags: Danh sách các tag mới
            custom_fields: Danh sách các trường tùy chỉnh mới
                Mỗi trường có dạng:
                {
                    "custom_field_id": int,
                    "custom_field_value_id": int,
                    "label": str,
                    "data_type": str,
                    "data_values": Any,
                    "value": str
                }
        
        Returns:
            Dict chứa thông tin khách hàng đã cập nhật
            
        Example:
            update_customer(
                customer_id=989898938,
                first_name="Chu",
                last_name="Manh",
                email="example@gmail.com",
                phone="0943555666",
                note="Ghi chu",
                tags=["Tag"],
                custom_fields=[
                    {
                        "custom_field_id": 27,
                        "custom_field_value_id": 829,
                        "label": "Test_Date",
                        "data_type": "DATE",
                        "data_values": None,
                        "value": ""
                    }
                ]
            )
        """
        data = {
            "customer": {
                "customer_id": customer_id
            }
        }
        
        # Chỉ thêm các trường được cung cấp vào request
        if first_name is not None:
            data["customer"]["first_name"] = first_name
        if last_name is not None:
            data["customer"]["last_name"] = last_name
        if email is not None:
            data["customer"]["email"] = email
        if phone is not None:
            data["customer"]["phone"] = phone
        if note is not None:
            data["customer"]["note"] = note
        if tags is not None:
            data["customer"]["tags"] = tags
        if custom_fields is not None:
            data["customer"]["custom_fields"] = custom_fields
        
        response = requests.post(
            f"{BASE_URL}/customer/update",
            headers=headers,
            json=data
        )
        return handle_api_response(response)

    @mcp.tool()
    def delete_customer(customer_id: int) -> Dict:
        """
        Xóa một khách hàng.
        
        Lưu ý quan trọng:
        1. Hành động này không thể hoàn tác
        2. Tất cả dữ liệu của khách hàng sẽ bị xóa vĩnh viễn
        
        Args:
            customer_id: ID của khách hàng cần xóa
        
        Returns:
            Dict chứa kết quả xóa khách hàng
            
        Example:
            delete_customer(989898940)
        """
        data = {
            "customer_id": customer_id
        }
        
        response = requests.post(
            f"{BASE_URL}/customer/delete",
            headers=headers,
            json=data
        )
        return handle_api_response(response)


        """
        Search customers by keyword.
        
        This tool searches through:
        - Customer names
        - Email addresses
        - Phone numbers
        - Company names
        - Tax codes
        
        The search is case-insensitive and supports partial matches.
        
        Args:
            keyword: Search keyword to match against customer fields
            page: Page number (default: 1)
            limit: Number of items per page (default: 10, max: 100)
        
        Returns:
            Dict containing:
            - items: List of matching customer objects
            - total: Total number of matches
            - page: Current page number
            - limit: Items per page
            
        Example:
            search_customers(
                keyword="john",  # Will match "John Doe", "john@example.com", etc.
                page=1,
                limit=20
            )
        """
        response = requests.get(
            f"{BASE_URL}/customers/search",
            headers=headers,
            params={
                "keyword": keyword,
                "page": page,
                "limit": limit
            }
        )
        return handle_api_response(response)


        """
        Import multiple customers in bulk.
        
        This tool allows importing multiple customers at once.
        Each customer in the list should follow the same format as create_customer().
        
        Args:
            customers: List of customer data dictionaries. Each dictionary should contain:
                - name: Customer name (required)
                - email: Email address (required, must be unique)
                - phone: Phone number (required, must be unique)
                - Other fields are optional
                
        Returns:
            Dict containing:
            - success: Number of successfully imported customers
            - failed: Number of failed imports
            - errors: List of errors for failed imports
            
        Example:
            import_customers([
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "birthday": "1990-01-01",
                    "gender": "male"
                },
                {
                    "name": "Jane Doe",
                    "email": "jane@example.com",
                    "phone": "+0987654321",
                    "company_name": "Example Corp"
                }
            ])
        """
        response = requests.post(
            f"{BASE_URL}/customers/import",
            headers=headers,
            json={"customers": customers}
        )
        return handle_api_response(response)


        """
        Delete a customer group.
        
        Important notes:
        1. Cannot delete groups that have customers
        2. This action cannot be undone
        3. Group deletion does not affect the customers previously in the group
        
        Args:
            group_id: The unique identifier of the group to delete (format: group_*)
        
        Returns:
            Dict containing the deletion confirmation
            
        Example:
            delete_customer_group("group_123")
        """
        response = requests.delete(
            f"{BASE_URL}/customers/groups/{group_id}",
            headers=headers
        )
        return handle_api_response(response) 