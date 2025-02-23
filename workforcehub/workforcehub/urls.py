from django.urls import path
from django.contrib import admin

from personal_data.views import UserAuthViewSet

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("auth/", UserAuthViewSet.as_view({
        "get": "verify_token",  # 토큰 검증 및 사용자 확인        
    })),
]