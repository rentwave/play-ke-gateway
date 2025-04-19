from django.db.models import Q, QuerySet
from django.db import models
from django.contrib.contenttypes.models import ContentType
from typing import Any, Dict, Type, Optional, Union

from api.utils.servicebase import ServiceBase


class ServiceRegistry:
	"""
	Registry to handle CRUD operations for different models.
	"""
	
	def get_model_class(self, model_name: str) -> Type[models.Model]:
		"""
		Get the model class based on the model name.
		"""
		try:
			# Use filter to avoid MultipleObjectsReturned error and pick the first match
			content_type = ContentType.objects.filter(model=model_name.lower()).first()
			if content_type:
				model_class = content_type.model_class()
				print(model_class)
				return model_class
			else:
				raise ValueError(f"Model '{model_name}' is not recognized.")
		except ContentType.DoesNotExist:
			raise ValueError(f"Model '{model_name}' is not recognized.")
	
	def get_service(self, model: Type[models.Model]) -> ServiceBase:
		"""
		Create and return a service instance for the given model.
		:param model: The model class (e.g., State, Corporate).
		:return: A ServiceBase instance configured for the model.
		"""
		return ServiceBase(manager=model.objects)
	
	def database(self, model_name: str, operation: str, instance_id: Optional[Any] = None,
	             data: Optional[Union[Dict[str, Any], Q]] = None,
	             soft: bool = True, additional_filters: Optional[Dict[str, Any]] = None) -> Any:
		"""
		Perform CRUD operations dynamically based on the model name and operation.
		Supports both dictionary-based and Q-object-based filtering, with additional filters.
		"""
		model_class = self.get_model_class(model_name)
		service = self.get_service(model_class)
		
		if data is None:
			data = {}
		
		if operation == 'create':
			return service.create(**data)
		elif operation == 'get':
			if not data:
				raise ValueError("Filter criteria must be provided for 'get' operation.")
			return service.get(**data)
		elif operation == 'update':
			if instance_id is None:
				raise ValueError("Instance ID is required for 'update' operation.")
			return service.update(instance_id, **data)
		elif operation == 'delete':
			if instance_id is None:
				raise ValueError("Instance ID is required for 'delete' operation.")
			return service.delete(instance_id, soft=soft)
		elif operation == 'filter':
			query = Q()
			if isinstance(data, Q):
				query &= data
			elif isinstance(data, dict):
				query &= Q(**data)
			else:
				raise ValueError("Data for 'filter' operation must be a Q object or dictionary.")
			if additional_filters:
				query &= Q(**additional_filters)
			return service.manager.filter(query)
		elif operation == 'all':
			return service.get_all_records()
		else:
			raise ValueError(f"Unsupported operation: {operation}")
	
	def build_queries(self, model_name: str, query: Q, additional_filters: Optional[Dict[str, Any]] = None) -> QuerySet:
		"""
		Filter records using a Q object for advanced querying.
		:param model_name: The name of the model class (e.g., 'state', 'corporate').
		:param query: The Q object for advanced query.
		:param additional_filters: Optional dictionary of additional filters to apply.
		:return: A QuerySet of filtered records.
		"""
		return self.database(model_name, 'filter', data=query, additional_filters=additional_filters)

