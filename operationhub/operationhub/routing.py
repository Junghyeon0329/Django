from django.urls import re_path
from operation_action import userchat

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<email>\w+)/$', userchat.ChatConsumer.as_asgi()),
]