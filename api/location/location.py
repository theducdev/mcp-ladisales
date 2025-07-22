"""
Location-related API tools for LaDiSales.
"""

from typing import Dict
import requests
from mcp.server.fastmcp import FastMCP
from ..common.common import BASE_LOCATION_URL, headers, handle_api_response

def register_location_tools(mcp: FastMCP):
    """Register all location-related tools with the MCP server."""
    
    @mcp.tool()
    def list_country() -> Dict:
        """
        Lấy danh sách các quốc gia.
        
        Returns:
            Dict chứa danh sách các quốc gia với thông tin:
            - country_code: Mã quốc gia
            - country_name: Tên quốc gia
            
        Example:
            list_country()
        """
        response = requests.post(
            f"{BASE_LOCATION_URL}/address/country/list",
            headers=headers
        )
        return handle_api_response(response)

    @mcp.tool()
    def list_state(country_code: str) -> Dict:
        """
        Lấy danh sách các tỉnh/thành phố của một quốc gia.
        
        Args:
            country_code: Mã quốc gia (ví dụ: "VN" cho Việt Nam)
        
        Returns:
            Dict chứa danh sách các tỉnh/thành phố với thông tin:
            - state_id: ID của tỉnh/thành phố
            - state_name: Tên tỉnh/thành phố
            
        Example:
            list_state("VN")
        """
        data = {
            "country_code": country_code
        }
        
        response = requests.post(
            f"{BASE_LOCATION_URL}/address/state/list",
            headers=headers,
            json=data
        )
        return handle_api_response(response)

    @mcp.tool()
    def list_district(country_code: str, state_id: int) -> Dict:
        """
        Lấy danh sách các quận/huyện của một tỉnh/thành phố.
        
        Args:
            country_code: Mã quốc gia (ví dụ: "VN" cho Việt Nam)
            state_id: ID của tỉnh/thành phố (ví dụ: 201 cho Hà Nội)
        
        Returns:
            Dict chứa danh sách các quận/huyện với thông tin:
            - district_id: ID của quận/huyện
            - district_name: Tên quận/huyện
            
        Example:
            list_district("VN", 201)
        """
        data = {
            "country_code": country_code,
            "state_id": state_id
        }
        
        response = requests.post(
            f"{BASE_LOCATION_URL}/address/district/list",
            headers=headers,
            json=data
        )
        return handle_api_response(response)

    @mcp.tool()
    def list_ward(country_code: str, state_id: int, district_id: int) -> Dict:
        """
        Lấy danh sách các phường/xã của một quận/huyện.
        
        Args:
            country_code: Mã quốc gia (ví dụ: "VN" cho Việt Nam)
            state_id: ID của tỉnh/thành phố (ví dụ: 201 cho Hà Nội)
            district_id: ID của quận/huyện (ví dụ: 1482 cho Quận Bắc Từ Liêm)
        
        Returns:
            Dict chứa danh sách các phường/xã với thông tin:
            - ward_id: ID của phường/xã
            - ward_name: Tên phường/xã
            
        Example:
            list_ward("VN", 201, 1482)
        """
        data = {
            "country_code": country_code,
            "state_id": state_id,
            "district_id": district_id
        }
        
        response = requests.post(
            f"{BASE_LOCATION_URL}/address/ward/list",
            headers=headers,
            json=data
        )
        return handle_api_response(response)
