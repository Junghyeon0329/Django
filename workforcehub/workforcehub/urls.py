from django.contrib import admin
from django.urls import path, include

from personal_data.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

# urlpatterns = [path('admin/', admin.site.urls),]
urlpatterns = [path('', include(router.urls)),]