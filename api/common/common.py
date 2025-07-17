"""
Common utilities and configurations for LaDiSales API.
"""

from typing import Dict
import requests

# API Configuration
BASE_URL = "https://apiv5.sales.ldpform.net/2.0/api"
API_KEY = "NzUeck7WdeqwUzdexKMVVd0Y"

headers = {
    "Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def handle_api_response(response: requests.Response) -> Dict:
    """
    Handle API response and raise exceptions if needed.
    
    Args:
        response: The response object from requests
        
    Returns:
        Dict: The JSON response data if successful
        
    Raises:
        Exception: If the response status code is >= 400
    """
    try:
        if response.status_code >= 400:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        return response.json()
    except requests.exceptions.SSLError:
        # Retry without SSL verification if SSL error occurs
        print("SSL Error occurred. Retrying without verification...")
        response = requests.request(
            response.request.method,
            response.request.url,
            headers=response.request.headers,
            json=response.request.body,
            verify=False
        )
        if response.status_code >= 400:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        return response.json() 