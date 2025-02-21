from django.urls import re_path
from operation_action import userchat

websocket_urlpatterns = [
    re_path(r'ws/chat/$', userchat.ChatConsumer.as_asgi()),  # WebSocket 엔드포인트 설정
]