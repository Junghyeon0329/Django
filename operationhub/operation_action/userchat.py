import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import MessageSerializer
from rest_framework import response, views, status
from .models import Message

class ChatHistoryAPIView(views.APIView):
    def get(self, request, email):
        # 이메일에 해당하는 메시지들을 필터링
        messages = Message.objects.filter(receiver_email=email).order_by('timestamp')
        
        # 메시지가 없으면 빈 리스트 반환
        if not messages:
            return response.Response({"messages": []}, status=status.HTTP_200_OK)

        # 메시지를 직렬화하여 반환
        serializer = MessageSerializer(messages, many=True)
        return response.Response({"messages": serializer.data}, status=status.HTTP_200_OK)


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.email = self.scope['url_route']['kwargs']['email']
        self.room_name = f"chat_{self.email}"
        self.room_group_name = f"chat_{self.email}"

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
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

