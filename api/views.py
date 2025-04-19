from django.http import JsonResponse
from api.models import AccessToken
from api.utils.common import get_request_data
from api.utils.registry import ServiceRegistry
from django.views.decorators.csrf import csrf_exempt
import secrets
from api.utils.response_provider import ResponseProvider

@csrf_exempt
def regenerate_oauth_client_secret(request):
	if request.method != 'POST':
		return JsonResponse({'error': 'Only POST allowed'}, status=405)
	payload = get_request_data(request)
	if isinstance(payload, JsonResponse):
		return payload
	client_id = payload.get('client_id')
	if not client_id:
		return JsonResponse({'error': 'Missing client_id'}, status=400)
	registry = ServiceRegistry()
	try:
		client = registry.database(
			model_name='oauthclient',
			operation='get',
			data={'client_id': client_id}
		)
		client.regenerate_credentials()
		return ResponseProvider(
			data={'client_id': client.client_id, 'client_secret': client.client_secret},
			message="Client secret regenerated",
			code=200
		).success()
	except Exception as e:
		return ResponseProvider(
			data={'error': str(e)},
			message="Error regenerating client secret",
			code=500
		).exception()

@csrf_exempt
def generate_oauth_token(request):
	if request.method != 'POST':
		return JsonResponse({'error': 'Only POST allowed'}, status=405)
	client_id = request.headers.get('Client-ID')
	client_secret = request.headers.get('Client-Secret')
	if not client_id or not client_secret:
		return JsonResponse({'error': 'Missing client_id or client_secret in headers'}, status=400)
	registry = ServiceRegistry()
	try:
		client = registry.database(
			model_name='oauthclient',
			operation='get',
			data={'client_id': client_id, 'client_secret': client_secret}
		)
		token_str = secrets.token_hex(50)
		access_token = registry.database(
			model_name='accesstoken', operation='create',
			data={'client': client, 'token': token_str, 'expires_in': 3600, 'state': client.state}
		)
		return ResponseProvider(
			data={'access_token': access_token.token, 'expires_in': access_token.expires_in, 'token_type': 'Bearer'},
			message="Token generated successfully", code=200
		).success()
	except Exception as e:
		return ResponseProvider(data={'error': str(e)}, message="Error generating access token", code=500).exception()

from django.urls import re_path

urlpatterns = [
	re_path(r'regenerate_credentials/', regenerate_oauth_client_secret, name='regenerate_credentials'),
	re_path(r'token/', generate_oauth_token, name='token'),
]


