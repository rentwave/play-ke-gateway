from django.views.decorators.csrf import csrf_exempt
import json
import requests
from api.backend.process import APIGatewayClient
from api.utils.common import get_request_data
from api.utils.decorators import auth_required
from api.utils.response_provider import ResponseProvider

class APIGateway(ResponseProvider):
    """API Gateway for dynamic routing and forwarding requests to target systems."""
    
    @csrf_exempt
    @auth_required
    def dynamic_api_gateway(self, request):
        try:
            payload = get_request_data(request)
            target_data = payload.get("target_system")
            route_data = payload.get("route")
            actual_data = payload.get("data", {})
            file_data = payload.get("files", {})
            if not target_data or not route_data:
                return ResponseProvider(
                    message="Missing target_system or route",
                    code="missing_fields"
                ).bad_request()
            target_query = {"name": target_data["name"]}
            existing_target = self.registry.database("TargetSystem", "filter", data=target_query)
            if not existing_target.exists():
                return ResponseProvider(
                    message="target_system does not exist",
                    code="404.000"
                ).bad_request()
            target_instance = existing_target.first()
            route_query = {"path": route_data["path"], "method": route_data["method"].upper()}
            existing_route = self.registry.database("Route", "filter", data=route_query)
            if existing_route.exists():
                route_instance = existing_route.first()
                updates = {}
                if route_instance.forward_path != route_data["path"]:
                    updates["forward_path"] = route_data["path"]
                if route_instance.target_id != target_instance.id:
                    updates["target"] = target_instance
                if updates:
                    route_instance = self.registry.database("Route", "update", instance_id=route_instance.id,
                                                            data=updates)
            else:
                route_data["method"] = route_data["method"].upper()
                route_data["target"] = target_instance
                route_data["forward_path"] = route_data["path"]
                route_instance = self.registry.database("Route", "create", data=route_data)
            forward_url = f"{target_instance.base_url.rstrip('/')}/{route_instance.forward_path.lstrip('/')}"
            client = APIGatewayClient(target_system=target_instance, forward_url=forward_url)
            method = route_instance.method
            forward_payload = {
                "data": actual_data,
                "files": {k: open(v, 'rb') for k, v in file_data.items()} if file_data else None
            }
            try:
                response = client.send(route_instance.forward_path, forward_payload)
            except requests.RequestException as e:
                return ResponseProvider(
                    message=f"Failed to forward request: {str(e)}",
                    code="forwarding_error"
                ).exception()
            content_type = response.headers.get("Content-Type", "")
            body = response.json() if content_type.startswith("application/json") else response.text
            return ResponseProvider(data={
                "target_system": {
                    "id": target_instance.id,
                    "name": target_instance.name,
                    "base_url": target_instance.base_url
                },
                "route": {
                    "id": route_instance.id,
                    "path": route_instance.path,
                    "method": route_instance.method,
                    "forward_path": route_instance.forward_path
                },
                "forwarded_response": {
                    "status_code": response.status_code,
                    "body": body
                }
            }).success()
        except json.JSONDecodeError:
            return ResponseProvider(message="Invalid JSON body", code="invalid_json").bad_request()
        except Exception as e:
            return ResponseProvider(message=str(e), code="unexpected_error").exception()


from django.urls import re_path

urlpatterns = [
	re_path(r'proxy/', APIGateway().dynamic_api_gateway, name='proxy'),
]

        