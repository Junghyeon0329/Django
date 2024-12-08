"""
URL configuration for operationhub project.

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
from django.urls import path

from operation_action.views import UserAPIView
from operation_action.workforce import WorkforceAPIView
from operation_action.logins import LoginAPIView
from rest_framework_simplejwt import views as jwt_views


''' 관리자를 추가하는 방법 : python manage.py createsuperuser '''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', UserAPIView.as_view(), name='info-api'),
    path('users/', WorkforceAPIView.as_view(), name='user-api'),
    path('login/', LoginAPIView.as_view(), name='login-api'),    
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]
    
