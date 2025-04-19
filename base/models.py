"""Base module models"""
from __future__ import unicode_literals

import uuid
from django.db import models


class BaseModel(models.Model):
    """
	Define repetitive methods to avoid cycles of redefining in every model.
	"""
    id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta(object):
        """Meta"""
        abstract = True


class GenericBaseModel(BaseModel):
    """
	Define repetitive methods to avoid cycles of redefining in every model.
	"""
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta(object):
        """Meta"""
        abstract = True


class State(GenericBaseModel):
    """
	Defines the different states used in the system e.g. Active, Disabled etc
	"""

    def __str__(self):
        return '%s' % self.name


    class Meta(object):
        """Meta"""
        ordering = ('name',)

    @classmethod
    def default_state(cls):
        """
		The default Active state. Help in ensuring that the admin will be created without supplying the state at the
		command like.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
        try:
            state = cls.objects.get(name="Active")
            return state
        except Exception:
            pass
        return None

    @classmethod
    def disabled_state(cls):
        """
		The default Disabled state. Help in ensuring that the admin will be created without supplying the state at the
		command like.
		@return: The active state, if it exists, or create a new one if it doesn't exist.
		@rtype: str | None
		"""
        try:
            state = cls.objects.get(name="Disabled")
            return state
        except Exception:
            pass
