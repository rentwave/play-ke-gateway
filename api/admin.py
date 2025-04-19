from django.contrib import admin
from .models import TargetSystem, Route, OAuthClient, AccessToken

@admin.register(TargetSystem)
class TargetSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'state')
    list_filter = ('state',)
    
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'target', 'forward_path', 'state')
    list_filter = ('method', 'target', 'state')
    search_fields = ('path', 'forward_path')

@admin.register(OAuthClient)
class OAuthClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_id', 'state')
    readonly_fields = ('client_id', 'client_secret')
    search_fields = ('name', 'client_id')
    actions = ['regenerate_client_secrets']
    list_filter = ('state',)
    
    @admin.action(description="Regenerate client credentials for selected clients")
    def regenerate_client_secrets(self, request, queryset):
        for client in queryset:
            client.regenerate_credentials()
        self.message_user(request, "Client credentials regenerated.")

@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('client', 'token', 'created_at', 'expires_in', 'is_valid', 'state')
    readonly_fields = ('token', 'created_at')
    list_filter = ('state',)
	
