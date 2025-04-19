from django.db import models
from base.models import BaseModel, GenericBaseModel, State


class TargetSystem(GenericBaseModel):
    name = models.CharField(max_length=100)
    base_url = models.URLField()
    auth_url = models.URLField(null=True, blank=True)
    auth_type = models.CharField(max_length=50, null=True, blank=True)
    app = models.CharField(max_length=100, null=True, blank=True)
    consumer_key = models.CharField(max_length=600, null=True, blank=True)
    consumer_secret = models.CharField(max_length=600, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=State.default_state)

    def __str__(self):
        return self.name

class Route(BaseModel):
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=[
        ('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')])
    target = models.ForeignKey(TargetSystem, on_delete=models.CASCADE)
    forward_path = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=State.default_state)

    def __str__(self):
        return f"{self.method} {self.path}"

class RequestLog(BaseModel):
    content_type = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    request_body = models.TextField()
    response_body = models.TextField()
    status_code = models.IntegerField()
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=State.default_state)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"[{self.status_code}] {self.method} {self.path} @ {self.date_created.strftime('%Y-%m-%d %H:%M:%S')}"

