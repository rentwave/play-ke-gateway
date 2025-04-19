import base64
import traceback
import requests


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

    def __make_request(self, method, endpoint, data=None, files=None, params=None):
        """Handles requests to target endpoint with optional data and files."""
        try:
            if str(self.target_system.base_url).endswith("/"):
                url = f"{self.target_system.base_url}{endpoint.lstrip('/')}"
            else:
                url = f"{self.target_system.base_url}/{endpoint.lstrip('/')}"
            headers = {}
            basic_auth = self._basic_auth()
            if basic_auth:
                headers["Authorization"] = f"Basic {basic_auth}"
            if method == "GET":
                response = requests.get(url, params=params or data, headers=headers, verify=False, timeout=300)
            elif method == "POST":
                if files:
                    response = requests.post(url, data=data, files=files, headers=headers, verify=False, timeout=300)
                else:
                    response = requests.post(url, json=data, headers=headers, verify=False, timeout=300)
            elif method == "PUT":
                if files:
                    response = requests.put(url, data=data, files=files, headers=headers, verify=False, timeout=300)
                else:
                    response = requests.put(url, json=data, headers=headers, verify=False, timeout=300)
            elif method == "DELETE":
                response = requests.delete(url, json=data, headers=headers, verify=False, timeout=300)
            else:
                raise ValueError(f"Unsupported method: {method}")
            return response
        except Exception as e:
            print("API Gateway Exception: %s", traceback.format_exc())
            return {"code": "500.500.0001", "message": "API Gateway request failed with exception"}

    def send(self, route, payload):
        """Public method to send data to the desired route on the target system."""
        data = payload.get("data", {})
        files = payload.get("files", None)
        if files:
            params = payload.get("params", None)
            method = getattr(self.target_system, "method", "POST").upper()
            return self.__make_request(method=method, endpoint=route, data=data, files=files, params=params)
        else:
            method = getattr(self.target_system, "method", "POST").upper()
            return self.__make_request(method=method, endpoint=route, data=data)
