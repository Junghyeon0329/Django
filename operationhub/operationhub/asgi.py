import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operationhub.settings')
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from operationhub.routing import websocket_urlpatterns


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
# python manage.py runserver
# daphne operationhub.asgi:application
# daphne -b 0.0.0.0 -p 9000 operationhub.asgi:application
