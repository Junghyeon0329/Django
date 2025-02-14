import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import MessageSerializer
from rest_framework import response, views, status
from .models import Message, User
from django.db.models import Q
from channels.db import database_sync_to_async
from datetime import datetime

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


active_connections = {}  # 현재 WebSocket에 연결된 사용자 관리

import jwt
from django.conf import settings
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        """ 웹소켓 연결 시 실행됨 """
        query_string = self.scope["query_string"].decode()
        token = dict(q.split("=") for q in query_string.split("&")).get("token")
        
        if not token:
            print("❌ WebSocket 연결 실패: 토큰이 없음")
            await self.close()
            return

        # 🔹 JWT 토큰 검증
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            self.user_id = payload["user_id"]  # JWT에서 user_id 추출
        except jwt.ExpiredSignatureError:
            print("❌ WebSocket 연결 실패: 토큰 만료됨")
            await self.close()
            return
        except jwt.DecodeError:
            print("❌ WebSocket 연결 실패: 토큰 검증 실패")
            await self.close()
            return

        # 🔹 사용자 정보 가져오기 (user_id로 조회)
        self.user = await self.get_user_by_id(self.user_id)

        if not self.user:
            print("❌ WebSocket 연결 실패: 사용자 정보 없음")
            await self.close()
            return

        # 현재 연결을 active_connections에 저장
        active_connections[self.user.email] = self.channel_name
        await self.accept()
        print(f"✅ {self.user.email} 웹소켓 연결됨")
            
    async def receive(self, text_data):
        """ 클라이언트로부터 메시지를 받을 때 실행됨 """
        text_data_json = json.loads(text_data)
                
        message_text = text_data_json.get('text')
        sender_email = text_data_json.get('sender_email')
        receiver_email = text_data_json.get('receiver_email')

        if sender_email and receiver_email and message_text:
            try:
                sender = await self.get_user_by_email(sender_email)
                receiver = await self.get_user_by_email(receiver_email)
                if sender and receiver:
                    message = Message(sender=sender, receiver_email=receiver.email, text=message_text)
                    await self.save_message(message)
                    
                    # 본인에게 메시지 전송
                    await self.send(text_data=json.dumps({
                        'message': {
                            'text': message_text,
                            'sender_email': sender_email,
                            'receiver_email': receiver_email,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        }
                    }))

                    # 상대방이 WebSocket에 연결되어 있으면 메시지 전송
                    if receiver.email in active_connections:
                        await self.channel_layer.send(
                            active_connections[receiver.email],
                            {
                                'type': 'chat_message',
                                'message': message_text,
                                'sender_email': sender_email,
                                'receiver_email': receiver_email,
                            }
                        )
                    else:
                        print(f"⚠️ {receiver_email}님이 현재 온라인 상태가 아님.")

                else:
                    print("❌ Sender or Receiver not found")

            except Exception as e:
                print(f"❌ Error: {e}")

        else:
            print("⚠️ Invalid message data")
    
    @database_sync_to_async
    def save_message(self, message):
        message.save()

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        """ user_id로 사용자 정보 가져오기 """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
    @database_sync_to_async
    def get_user_by_email(self, email):        
        try:
            return User.objects.get(email=email)            
        except User.DoesNotExist:
            return None
    
    async def chat_message(self, event):
        """ WebSocket을 통해 메시지 전송 """
        await self.send(text_data=json.dumps({
            'message': {
                'text': event['message'],
                'sender_email': event['sender_email'],
                'receiver_email': event['receiver_email'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        }))
   
    async def disconnect(self, close_code):
        """ 웹소켓 연결이 종료될 때 실행됨 """
        if self.email in active_connections:
            del active_connections[self.email]  # 연결 제거
        print(f"🔴 {self.email} 웹소켓 연결 종료")
