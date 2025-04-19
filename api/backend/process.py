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
            request_args = {
                "url": url,
                "headers": headers,
                "verify": False,
                "timeout": 300
            }

            if method == "GET":
                request_args["params"] = params or data
                response = requests.get(**request_args)
            elif method in ["POST", "PUT"]:
                if files:
                    request_args["data"] = data
                    request_args["files"] = files
                else:
                    request_args["json"] = data
                response = getattr(requests, method.lower())(**request_args)
            elif method == "DELETE":
                request_args["json"] = data
                response = requests.delete(**request_args)
            else:
                raise ValueError(f"Unsupported method: {method}")

            return response
        except Exception:
            print("API Gateway Exception:\n", traceback.format_exc())
            raise

    def send(self, route, payload):
        """Public method to send data to the desired route on the target system."""
        data = payload.get("data", {})
        files = payload.get("files", None)
        method = getattr(self.target_system, "method", "POST").upper()
        return self.__make_request(method=method, endpoint=route, data=data, files=files)
