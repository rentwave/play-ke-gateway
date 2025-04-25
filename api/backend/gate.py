from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from api.backend.process import APIGatewayClient
from api.utils.common import get_request_data
from api.utils.response_provider import ResponseProvider


class APIGateway(ResponseProvider):
    """API Gateway for dynamic routing and forwarding requests to target systems."""
    
    @csrf_exempt
    def dynamic_api_gateway(self, request):
        try:
            content_type = request.content_type
            if content_type == 'application/json':
                body = get_request_data(request)
                print(body)
                route = body.get('route')
                actual_data = body.get('data', {})
                uploaded_file = None
            elif content_type.startswith('multipart/form-data'):
                route = request.POST.get('route')
                actual_data = {k: v for k, v in request.POST.items() if k != 'route'}
                uploaded_file = request.FILES.get('file')
            else:
                return ResponseProvider(data={'message': 'Unsupported Content-Type'}).bad_request()
            if not route:
                return ResponseProvider(data={'message': 'Missing route'}).bad_request()
            url_parts = route.strip('/').split('/')
            if not url_parts:
                return ResponseProvider(data={'message': 'Invalid route format'}).bad_request()
            app = url_parts.pop(0)
            url = '/'.join(url_parts)
            print("url_parts", url)
            if not url.endswith('/'):
                url += '/'
            if  not route:
                return ResponseProvider(
                    message="Missing target_system or route",
                    code="missing_fields"
                ).bad_request()
            target_query = {"app": app}
            existing_target = self.registry.database("TargetSystem", "filter", data=target_query)
            if not existing_target.exists():
                return ResponseProvider(
                    message="target_system does not exist",
                    code="404.000"
                ).bad_request()
            target_instance = existing_target.first()
            route_query = {
                "path": url,
                "method": "POST",
            }
            existing_route = self.registry.database("Route", "filter", data=route_query)
            if existing_route.exists():
                route_instance = existing_route.first()
                updates = {}
                if route_instance.forward_path != url:
                    updates["forward_path"] = url
                if route_instance.target_id != target_instance.id:
                    updates["target"] = target_instance
                if updates:
                    route_instance = self.registry.database(
                        "Route", "update", instance_id=route_instance.id, data=updates
                    )
            else:
                route_query["method"] = "POST"
                route_query["target"] = target_instance
                route_query["forward_path"] = url
                route_instance = self.registry.database("Route", "create", data=route_query)
            forward_url = f"{target_instance.base_url.rstrip('/')}/{route_instance.forward_path.lstrip('/')}"
            client = APIGatewayClient(target_system=target_instance, forward_url=forward_url)
            files_for_forwarding = {
                'file': (uploaded_file.name, uploaded_file, uploaded_file.content_type)
            } if uploaded_file else None
            forward_payload = {
                "data": actual_data,
                "files": files_for_forwarding
            }
            try:
                response = client.send(route_instance.forward_path, forward_payload)
            except requests.RequestException as e:
                log_data = {
                    "content_type": content_type,
                    "method": request.method,
                    "path": request.path,
                    "request_body": json.dumps(actual_data, indent=2),
                    "response_body": str(e),
                    "status_code": 500,
                }
                self.registry.database("RequestLog", "create", data=log_data)
                return ResponseProvider(
                    message=f"Failed to forward request: {str(e)}",
                    code="forwarding_error"
                ).exception()
            response_content_type = response.headers.get("Content-Type", "")
            try:
                if response_content_type.startswith("application/json"):
                    body = response.json()
                else:
                    body = response.text
            except json.JSONDecodeError:
                body = response.text
            log_data = {
                "content_type": content_type,
                "method": request.method,
                "path": request.path,
                "request_body": json.dumps(actual_data, indent=2),
                "response_body": json.dumps(body, indent=2) if isinstance(body, dict) else str(body),
                "status_code": response.status_code,
            }
            self.registry.database("RequestLog", "create", data=log_data)
            return ResponseProvider(data={
                "status_code": response.status_code,
                "body": body
            }).success()
        except json.JSONDecodeError:
            return ResponseProvider(message="Invalid JSON body", code="invalid_json").bad_request()
        except Exception as e:
            log_data = {
                "content_type": request.content_type,
                "method": request.method,
                "path": request.path,
                "request_body": request.body.decode("utf-8") if request.body else "",
                "response_body": str(e),
                "status_code": 500,
            }
            self.registry.database("RequestLog", "create", data=log_data)
            return ResponseProvider(message=str(e), code="unexpected_error").exception()

from django.urls import re_path

urlpatterns = [
    re_path(r'post/', APIGateway().dynamic_api_gateway, name='proxy'),
]
