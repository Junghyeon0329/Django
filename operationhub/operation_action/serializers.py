from rest_framework import serializers
from .models import Message
        
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'text', 'timestamp', 'sender_email', 'receiver_email']

    def get_sender_email(self, obj):
        return obj.sender.email  # sender의 email 반환