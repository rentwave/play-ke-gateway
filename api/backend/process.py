import os
import base64
import traceback
import requests
import logging

lgr = logging.getLogger(__name__)

class APIGatewayClient:
    """Reusable API Gateway Client for handling requests to registered target systems."""

    def __init__(self, target_system, forward_url, username="", password=""):
        self.target_system = target_system
        self.forward_url = forward_url
        self.username = username
        self.password = password

    def _basic_auth(self):
        """Generate Basic Auth header value."""
        if not self.username or not self.password:
            return None
        credentials = f"{self.username}:{self.password}".encode("utf-8")
        return base64.b64encode(credentials).decode("utf-8")
    
    def __make_request(self, endpoint, **kwargs):
        """Utility function for handling all request"""
        try:
            if str(self.target_system.base_url).endswith("/"):
                url = ''.join([self.target_system.base_url, endpoint])
            else:
                url = ''.join([self.target_system.base_url, '/', endpoint])
            if not url.endswith("/"):
                url += "/"
            headers = {}
            return requests.post(url=url, json=kwargs, verify=False, timeout=300, headers=headers)
        except Exception as e:
            lgr.info(traceback.print_exc())
            return {"code": "500.500.0001", "message": "API Gateway request failed with exception"}

    def send(self, route, payload):
        """Public method to send data to the desired route on the target system."""
        return self.__make_request(route, **payload)
