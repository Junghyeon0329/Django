"""
URL configuration for workforcehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from personal_data.views import UserViewSet

# 127.0.0.1:8000/permissions/?page=1&page_size=2
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)

# urlpatterns = [path('admin/', admin.site.urls),]
urlpatterns = [path('', include(router.urls)),]