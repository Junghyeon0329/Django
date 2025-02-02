from rest_framework import serializers
from .models import Notice, UserProfile, Message
    
class NoticeSerializer(serializers.ModelSerializer):
    author_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'author_email', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_author_email(self, obj):
        return obj.author.email    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'profile_picture']
        
        
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'text', 'timestamp', 'sender_email', 'receiver_email']

    def get_sender_email(self, obj):
        return obj.sender.email  # sender의 email 반환