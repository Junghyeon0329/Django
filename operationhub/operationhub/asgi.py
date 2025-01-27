import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'operationhub.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

async def connect(self):
    print(f"Scope: {self.scope}")


# https://velog.io/@mimijae/Django-Django-rest-framework%EB%A1%9C-%EC%9B%B9%EC%86%8C%EC%BC%93-%EC%B1%84%ED%8C%85-%EC%84%9C%EB%B2%84-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B02