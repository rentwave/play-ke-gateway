import json
from datetime import datetime, date, timedelta
from decimal import Decimal

from django.http import QueryDict

from django.http import QueryDict
import json


def get_request_data(request):
	"""
	Retrieves the request data including file data regardless of request method or content type.
	@param request: The Django HttpRequest.
	@type request: WSGIRequest
	@return: A combined dict of data and files
	@rtype: dict
	"""
	try:
		data = {}
		content_type = request.META.get('CONTENT_TYPE', '')
		if content_type.startswith('application/json'):
			try:
				data = json.loads(request.body)
			except json.JSONDecodeError:
				data = {}
		elif content_type.startswith('multipart/form-data'):
			data = request.POST.copy()
			data = data.dict()
			if request.FILES:
				for key, file in request.FILES.items():
					data[key] = file
		elif request.method == 'GET':
			data = request.GET.copy()
			data = data.dict()
		elif request.method == 'POST':
			data = request.POST.copy()
			data = data.dict()
			if request.FILES:
				for key, file in request.FILES.items():
					data[key] = file
		if not data:
			try:
				data = json.loads(request.body)
			except Exception:
				data = {}
		return data
	except Exception as e:
		print(f'get_request_data Exception: {e}')
		return {}


def get_clean_request_data(request):
	"""
	Retrieves the request data irrespective of the method and type it was send stripping
	off any parameters not needed.
	@param request: The Django HttpRequest.
	@type request: WSGIRequest
	@return: The data from the request as a dict
	@rtype: QueryDict
	"""
	try:
		data = get_request_data(request)
		data.pop('target', None)
		data.pop('source_ip', None)
		data.pop('system', None)
		data.pop('token', None)
		data.pop('client_id', None)
		data.pop('client_secret', None)
		return data
	except Exception as e:
		print('get_clean_request_data Exception: %s', e)
	return QueryDict()


def json_super_serializer(obj):
	"""
	Automatic serializer for objects not serializable by default by the JSON serializer.
	Includes datetime, date, Decimal
	@param obj: The object to convert.
	@return: String of the data converted.
	@rtype: str
	"""
	if isinstance(obj, datetime):
		try:
			return obj.strftime('%d/%m/%Y %I:%M:%S %p')
		except Exception:
			return str(obj)
	elif isinstance(obj, date):
		try:
			return obj.strftime('%d/%m/%Y')
		except Exception:
			return str(obj)
	elif isinstance(obj, (Decimal, float)):
		return str("{:,}".format(round(Decimal(obj), 2)))
	elif isinstance(obj, timedelta):
		return obj.days
	return str(obj)
