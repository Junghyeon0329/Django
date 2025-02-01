import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from rest_framework import response

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.email = self.scope['url_route']['kwargs']['email']  # URL에서 이메일 가져오기
        self.room_name = f"chat_{self.email}"  # 이메일에 해당하는 채팅 방 이름
        self.room_group_name = f"chat_{self.email}"  # 이메일을 기반으로 한 방 그룹

        # WebSocket에 연결할 때, 채팅 방 그룹에 가입
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket 연결이 끊어지면, 채팅 방 그룹에서 나감
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # 클라이언트로부터 받은 메시지
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 메시지를 해당 채팅 방 그룹에 전달
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # 채팅 방 그룹으로부터 받은 메시지를 클라이언트에 전달
        message = event['message']

        # WebSocket으로 메시지 보내기
        await self.send(text_data=json.dumps({
            'message': message
        }))
