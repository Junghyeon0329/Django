import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import MessageSerializer
from rest_framework import response, views, status
from .models import Message, User
from django.db.models import Q
from channels.db import database_sync_to_async


class ChatHistoryAPIView(views.APIView):
    def post(self, request):
        my_email = request.data.get('myEmail')
        other_email = request.data.get('otherEmail')

        if not my_email or not other_email:
            return response.Response(
                {"detail": "Both 'myEmail' and 'otherEmail' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            my_user = User.objects.get(email=my_email)
            other_user = User.objects.get(email=other_email)
        except User.DoesNotExist:
            return response.Response(
                {"detail": "One or both users not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        messages = Message.objects.filter(
            (Q(sender=my_user) & Q(receiver_email=other_user)) |
            (Q(sender=other_user) & Q(receiver_email=my_user))
        ).order_by('timestamp')
        
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
                
        message_text = text_data_json.get('text')
        sender_email = text_data_json.get('sender_email')
        receiver_email = text_data_json.get('receiver_email')

        if sender_email and receiver_email and message_text:
            try:
                # 이메일을 통해 User 객체 가져오기
                sender = await self.get_user_by_email(sender_email)
                receiver = await self.get_user_by_email(receiver_email)
                if sender and receiver:
                    message = Message(sender=sender, receiver_email=receiver, text=message_text)
                    await self.save_message(message)
                else:
                    print("Sender or Receiver not found")

            except Exception as e:
                print(f"Error: {e}")

        else:
            print("Invalid message data")
    
    @database_sync_to_async
    def save_message(self, message):
        message.save()

    @database_sync_to_async
    def get_user_by_email(self, email):        
        try:
            return User.objects.get(email=email)            
        except User.DoesNotExist:
            return None
        
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    async def disconnect(self, close_code):
        pass

