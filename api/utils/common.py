from datetime import datetime, date, timedelta
from decimal import Decimal
import json
from django.http import QueryDict

def get_request_data(request):
    """
    Retrieves all request data, including form fields and files.
    @return: dict with keys 'data' and 'files'
    """
    try:
        if request.content_type.startswith('multipart/form-data'):
            data = request.POST.copy().dict()
            files = request.FILES.copy()
        elif request.content_type == 'application/json':
            data = json.loads(request.body)
            files = {}
        elif request.method == 'GET':
            data = request.GET.dict()
            files = {}
        else:
            try:
                data = json.loads(request.body)
                files = {}
            except Exception:
                data = {}
                files = {}
        return {"data": data, "files": files}
    except Exception as e:
        print(f"get_request_data Exception: {e}")
        return {"data": {}, "files": {}}

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
