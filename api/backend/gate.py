from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from api.backend.process import APIGatewayClient
from api.models import RequestLog
from api.utils.common import get_request_data
from api.utils.decorators import auth_required
from api.utils.response_provider import ResponseProvider


class APIGateway(ResponseProvider):
    """API Gateway for dynamic routing and forwarding requests to target systems."""
    
    @csrf_exempt
    @auth_required
    def dynamic_api_gateway(self, request):
        try:
            content_type = request.content_type
            if content_type == 'application/json':
                payload = get_request_data(request)
                uploaded_file = None
            elif content_type.startswith('multipart/form-data'):
                payload = {
                    'target_system': json.loads(request.POST.get('target_system', '{}')),
                    'route': json.loads(request.POST.get('route', '{}')),
                    'data': json.loads(request.POST.get('data', '{}')),
                }
                uploaded_file = request.FILES.get("file")
            else:
                return JsonResponse({'message': 'Unsupported Content-Type'}, status=400)
            route_data = payload.get("path")
            url_list = route_data.split("/")
            app = url_list.pop(0)
            url = "/".join(url_list)
            actual_data = payload.get("data", {})
            if  not route_data:
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
                "method": "POST", # Assuming POST method for simplicity
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
                route_data["method"] = "POST"
                route_data["target"] = target_instance
                route_data["forward_path"] = url
                route_instance = self.registry.database("Route", "create", data=route_data)
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
                RequestLog.objects.create(
                    content_type=content_type,
                    method=request.method,
                    path=request.path,
                    request_body=json.dumps(payload, indent=2),
                    response_body=str(e),
                    status_code=500
                )
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
            RequestLog.objects.create(
                content_type=content_type,
                method=request.method,
                path=request.path,
                request_body=json.dumps(payload, indent=2),
                response_body=json.dumps(body, indent=2) if isinstance(body, dict) else str(body),
                status_code=response.status_code
            )
            
            return ResponseProvider(data={
                "status_code": response.status_code,
                "body": body
            }).success()
        
        except json.JSONDecodeError:
            return ResponseProvider(message="Invalid JSON body", code="invalid_json").bad_request()
        except Exception as e:
            RequestLog.objects.create(
                content_type=request.content_type,
                method=request.method,
                path=request.path,
                request_body=request.body.decode("utf-8") if request.body else "",
                response_body=str(e),
                status_code=500
            )
            return ResponseProvider(message=str(e), code="unexpected_error").exception()


from django.urls import re_path

urlpatterns = [
    re_path(r'proxy/', APIGateway().dynamic_api_gateway, name='proxy'),
]
