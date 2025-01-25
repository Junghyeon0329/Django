# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # WebSocket 연결 요청이 오면 실행됩니다.
        self.room_name = 'chat_room'  # 예시로 고정된 방 이름 사용
        self.room_group_name = f'chat_{self.room_name}'  # 방 이름에 따라 그룹 설정

        # 방 그룹에 가입
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # WebSocket 연결 수락

    async def disconnect(self, close_code):
        # WebSocket 연결 종료 시 실행됩니다.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # 메시지를 받을 때 실행됩니다.
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 방 그룹에 메시지 보내기
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # 메시지 전송을 위한 이벤트 타입
                'message': message
            }
        )

    async def chat_message(self, event):
        # 방 그룹에서 메시지를 받았을 때 실행됩니다.
        message = event['message']

        # 클라이언트에 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message
        }))
