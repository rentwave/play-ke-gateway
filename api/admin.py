from django.contrib import admin
from .models import TargetSystem, Route,  RequestLog

@admin.register(TargetSystem)
class TargetSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'consumer_key', 'consumer_secret','app','state')
    list_filter = ('state',)
    
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'target', 'forward_path', 'state')
    list_filter = ('method', 'target', 'state')
    search_fields = ('path', 'forward_path')
#
# @admin.register(OAuthClient)
# class OAuthClientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'client_id', 'state')
#     readonly_fields = ('client_id', 'client_secret')
#     search_fields = ('name', 'client_id')
#     actions = ['regenerate_client_secrets']
#     list_filter = ('state',)
#
#     @admin.action(description="Regenerate client credentials for selected clients")
#     def regenerate_client_secrets(self, request, queryset):
#         for client in queryset:
#             client.regenerate_credentials()
#         self.message_user(request, "Client credentials regenerated.")
#
# @admin.register(AccessToken)
# class AccessTokenAdmin(admin.ModelAdmin):
#     list_display = ('client', 'token', 'created_at', 'expires_in', 'is_valid', 'state')
#     readonly_fields = ('token', 'created_at')
#     list_filter = ('state',)
	
@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("date_created", "method", "path", "status_code", "content_type")
    list_filter = ("status_code", "content_type", "method", "date_created")
    search_fields = ("path", "request_body", "response_body")
    readonly_fields = ("content_type", "method", "path", "request_body", "response_body", "status_code", "date_created")
    ordering = ("-date_created",)

    fieldsets = (
        (None, {
            "fields": ("date_created", "method", "path", "content_type", "status_code")
        }),
        ("Request Body", {
            "classes": ("collapse",),
            "fields": ("request_body",)
        }),
        ("Response Body", {
            "classes": ("collapse",),
            "fields": ("response_body",)
        }),
    )

    def has_add_permission(self, request):
        return False  # prevent manual creation

    def has_change_permission(self, request, obj=None):
        return False  # prevent editing