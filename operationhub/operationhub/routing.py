# from django.urls import re_path
# from operation_action import userchat

# websocket_urlpatterns = [
#     re_path(r'ws/chat/', userchat.ChatConsumer.as_asgi()),
# ]

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from operation_action import userchat

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             re_path(r"ws/chat/$", userchat.ChatConsumer.as_asgi()),
#         ])
#     ),
# })

websocket_urlpatterns = [
    re_path(r'ws/chat/$', userchat.ChatConsumer.as_asgi()),  # WebSocket 엔드포인트 설정
]