from typing import Any, Dict, Optional
from django.db import models
import logging
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

lgr = logging.getLogger(__name__)


class ServiceBase:
	"""
	Base service class to handle CRUD operations for a given model.
	"""
	
	manager: Optional[models.Manager] = None
	
	def __init__(self, manager: models.Manager, lock_for_update: bool = False, *args: Any,
	             **annotations: Dict[str, Any]):
		"""
		Initializes the service with the provided manager and optional annotations.
		:param manager: The model's manager instance (e.g., State.objects).
		:param lock_for_update: Whether to lock the rows for update.
		:param args: Arguments for additional annotations.
		:param annotations: Key-value pairs for annotations.
		"""
		self.manager = manager
		if lock_for_update:
			self.manager = self.manager.select_for_update()
		if args:
			for name, value in args:
				if isinstance(name, str):
					self.manager = self.manager.annotate(**{name: value})
		if annotations:
			self.manager = self.manager.annotate(**annotations)
	
	def get(self, *args: Any, **kwargs: Any) -> Optional[models.Model]:
		"""
		Retrieves a single record from the DB using the manager.
		"""
		lgr.debug('Fetching record with criteria: %s', kwargs)
		
		if not kwargs:
			lgr.error('No filter criteria provided for get() query.')
			return None
		try:
			return self.manager.get(*args, **kwargs)
		except MultipleObjectsReturned:
			lgr.warning('Multiple objects returned for criteria: %s. Returning the first one based on ID.', kwargs)
			return self.manager.filter(*args, **kwargs).order_by('id').first()
		except ObjectDoesNotExist:
			lgr.warning('Object not found with criteria: %s', kwargs)
		except Exception as e:
			lgr.exception('Error retrieving object with criteria %s: %s', kwargs, e)
		return None
	
	def filter(self, *args: Any, **kwargs: Any) -> Optional[models.QuerySet]:
		"""
		Returns a queryset of objects from the manager.
		:param args: Arguments for the filter method.
		:param kwargs: Key-value arguments for the filter method.
		:return: Queryset or None if error occurs.
		"""
		try:
			return self.manager.filter(*args, **kwargs)
		except Exception as e:
			lgr.exception('Error filtering objects with criteria %s: %s', kwargs, e)
		return None
	
	def create(self, **kwargs: Any) -> Optional[models.Model]:
		"""
		Creates an entry with the given kwargs for the manager.
		:param kwargs: Key-value arguments for the create method.
		:return: Created object or None if error occurs.
		"""
		try:
			return self.manager.create(**kwargs)
		except Exception as e:
			lgr.exception('Error creating object with data %s: %s', kwargs, e)
		return None
	
	def update(self, pk: Any, **kwargs: Any) -> Optional[models.Model]:
		"""
		Updates the record with the given primary key.
		:param pk: The primary key of the record to update.
		:param kwargs: Key-value arguments to update the record.
		:return: The updated record or None if not found or error occurs.
		"""
		return self._update_record(pk, kwargs, sync=True)
	
	def re_update(self, pk: Any, **kwargs: Any) -> Optional[models.Model]:
		"""
		Re-updates the record with the given primary key.
		:param pk: The primary key of the record to update.
		:param kwargs: Key-value arguments to update the record.
		:return: The updated record or None if not found or error occurs.
		"""
		return self._update_record(pk, kwargs, sync=False)
	
	def _update_record(self, pk: Any, kwargs: Dict[str, Any], sync: bool) -> Optional[models.Model]:
		"""
		Helper method to update the record with the given primary key.
		:param pk: The primary key of the record to update.
		:param kwargs: Key-value arguments to update the record.
		:param sync: Flag to determine if synchronization should be considered.
		:return: The updated record or None if not found or error occurs.
		"""
		try:
			record = self.get(id=pk)
			if record:
				for k, v in kwargs.items():
					setattr(record, k, v)
				if sync and hasattr(record, 'SYNC_MODEL') and record.SYNC_MODEL:
					record.synced = False
				record.save()
				record.refresh_from_db()
				return record
		except Exception as e:
			lgr.exception('Error updating record with pk %s: %s', pk, e)
		return None
	
	def delete(self, pk: Any, soft: bool = True) -> Optional[models.Model]:
		"""
		Deletes the record with the given primary key.
		:param pk: The primary key of the record to delete.
		:param soft: Boolean to determine if the delete should be soft or hard.
		:return: The deleted record or None if not found or error occurs.
		"""
		try:
			record = self.get(id=pk)
			if record:
				if soft and hasattr(record, 'is_active'):
					record.is_active = False
					record.deleted_at = timezone.now()
					record.save()
				else:
					record.delete()
				return record
		except Exception as e:
			lgr.exception('Error deleting record with pk %s: %s', pk, e)
		return None
	
	def get_all_records(self) -> models.QuerySet:
		"""
		Retrieve all instances of the model.
		:return: A queryset of all model instances.
		"""
		return self.manager.all()
