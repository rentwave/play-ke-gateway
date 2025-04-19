import json
from functools import wraps
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.http import HttpRequest
from api.models import AccessToken


def auth_required(view_func):
    """
    Validates Bearer token from Authorization header.
    Adds `request.client` and `request.token` if valid.
    """
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        request: HttpRequest = next((arg for arg in args if isinstance(arg, HttpRequest)), None)
        if request is None:
            return JsonResponse({'error': 'Invalid request'}, status=400)
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JsonResponse({'error': 'Unauthorized: Bearer token required'}, status=401)
        token_value = auth_header[len("Bearer "):].strip()
        if not token_value:
            return JsonResponse({'error': 'Unauthorized: Token missing'}, status=401)
        try:
            token = AccessToken.objects.select_related('client').get(token=token_value)
        except AccessToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid or unknown token'}, status=401)
        if not token.is_valid():
            return JsonResponse({'error': 'Token expired'}, status=401)
        if not token.client.is_active:
            return JsonResponse({'error': 'Client inactive'}, status=403)
        request.client = token.client
        request.token = token
        return view_func(*args, **kwargs)
    return wrapped_view
