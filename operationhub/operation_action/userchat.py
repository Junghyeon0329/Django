import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import MessageSerializer
from rest_framework import response, views, status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from .models import Message


class ChatHistoryAPIView(views.APIView):
    def get(self, request, email):
        
        messages = Message.objects.filter(receiver_email=email).order_by('timestamp')        
        if not messages:
            return response.Response({"messages": []}, status=status.HTTP_200_OK)

        serializer = MessageSerializer(messages, many=True)
        return response.Response({"messages": serializer.data}, status=status.HTTP_200_OK)


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.email = None

        await self.accept()
            
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        if text_data_json['type'] == 'authenticate':
            token = text_data_json['token']
            try:
                # JWT 토큰을 검증하고 이메일을 추출
                access_token = AccessToken(token)
                self.email = access_token['email']  # 이메일은 JWT에 포함되어 있어야 함

                if self.email:
                    self.room_group_name = f"chat_{self.email.replace('@', '-').replace('.', '-')}"
                    await self.channel_layer.group_add(
                        self.room_group_name,
                        self.channel_name
                    )
                    await self.send(text_data=json.dumps({
                        'type': 'authenticated',
                        'message': f'Hello, {self.email}!'
                    }))
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'Invalid email!'
                    }))
            except AuthenticationFailed:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Authentication failed.'
                }))
                
        # 나머지 메시지 처리
        elif text_data_json.get('type') == 'chat_message':
            message = text_data_json['message']
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

    async def disconnect(self, close_code):
        if self.email:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
