import secrets
from django.db import models
from base.models import BaseModel, GenericBaseModel, State

def generate_client_id():
    return secrets.token_urlsafe(50)

def generate_client_secret():
    return secrets.token_urlsafe(100)

class TargetSystem(GenericBaseModel):
    name = models.CharField(max_length=100)
    base_url = models.URLField()
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


class OAuthClient(GenericBaseModel):
    client_id = models.CharField(max_length=300, unique=True, default=generate_client_id())
    client_secret = models.CharField(max_length=500, unique=True, default=generate_client_secret())
    is_active = models.BooleanField(default=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=State.default_state)
    
    def regenerate_credentials(self):
        self.client_id = secrets.token_urlsafe(32)
        self.client_secret = secrets.token_urlsafe(64)
        self.save()

    def __str__(self):
        return getattr(self, "name", self.client_id)

class AccessToken(BaseModel):
    client = models.ForeignKey(OAuthClient, on_delete=models.CASCADE)
    token = models.CharField(max_length=300, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_in = models.IntegerField(default=3600)  # in seconds
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=State.default_state)

    def is_valid(self):
        from django.utils.timezone import now, timedelta
        return self.created_at + timedelta(seconds=self.expires_in) > now()

    def __str__(self):
        return f"{self.client.name} Token"

