from rest_framework import serializers
from .models import Notice, UserProfile
    
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