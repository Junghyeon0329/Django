import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.room_name = "chat_room"
    #     self.room_group_name = f"chat_{self.room_name}"

    #     # 그룹에 가입
    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     # WebSocket 연결 수락
    #     await self.accept()

    # async def disconnect(self, close_code):
    #     # 그룹에서 제거
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    async def receive(self, text_data):
                
        text_data_json = json.loads(text_data)        
        message = text_data_json['text']
        message_timestap = text_data_json['timestamp']
        print()
        print("message:",message, message_timestap)
        print()
        

        # 메시지를 그룹으로 전송
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    async def chat_message(self, event):
        # 그룹 메시지를 클라이언트로 전송
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
