"""
URL configuration for gateway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Customize the admin panel appearance
admin.site.site_header = "PLAY KE API Gateway Administration"
admin.site.site_title = "API Gateway Portal"
admin.site.index_title = "Welcome to PLAY KE API Gateway Management Dashboard"
admin.site.site_url = "/"


urlpatterns = [
    path('hq/', admin.site.urls),
    path('api/', include('api.backend.gate'), name='api-endpoints'),
    path('auth/', include('api.views'), name='auth'),
]
