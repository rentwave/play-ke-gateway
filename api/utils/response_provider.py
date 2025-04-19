from django.http import JsonResponse

from api.utils.common import json_super_serializer
from api.utils.registry import ServiceRegistry


class ResponseProvider:
	"""Provides standardized JSON responses.

	Status Codes:
	400 - Bad Request
	200 - Success
	401 - Unauthorized Access
	500 - Internal Server Error
	"""
	
	def __init__(self, data=None, message=None, code=None):
		self.data = data or {}
		if message:
			self.data["code"] = code
			self.data["message"] = message
		self.registry = ServiceRegistry()
	
	def _response(self, status):
		return JsonResponse(self.data, status=status, json_dumps_params={'default': json_super_serializer})
	
	def success(self):
		"""Return a success response (200)."""
		return self._response(status=200)
	
	def bad_request(self):
		"""Return a bad request response (400)."""
		return self._response(status=400)
	
	def unauthorized(self):
		"""Return an unauthorized response (401)."""
		return self._response(status=401)
	
	def exception(self):
		"""Return an internal server error response (500)."""
		return self._response(status=500)


