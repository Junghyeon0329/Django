import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import MessageSerializer
from rest_framework import response, views, status
from .models import Message
from django.db.models import Q

class ChatHistoryAPIView(views.APIView):
    def post(self, request):
        my_email = request.data.get('myEmail')
        other_email = request.data.get('otherEmail')

        if not my_email or not other_email:
            return response.Response(
                {"detail": "Both 'myEmail' and 'otherEmail' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 메시지를 주고받은 이메일 필터링
        messages = Message.objects.filter(
            (Q(sender__email=my_email) & Q(receiver_email=other_email)) |
            (Q(sender__email=other_email) & Q(receiver_email=my_email))
        ).order_by('timestamp')

        if not messages:
            return response.Response({"messages": []}, status=status.HTTP_200_OK)

        # 직렬화 후 반환
        serializer = MessageSerializer(messages, many=True)
        return response.Response({"messages": serializer.data}, status=status.HTTP_200_OK)

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.email = None
        await self.accept()
            
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
            
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
