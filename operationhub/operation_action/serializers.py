# board/serializers.py
from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        # 'author' 필드를 validated_data에 추가하여 저장
        validated_data['author'] = self.context['request'].user  # 로그인한 사용자 설정
        return super().create(validated_data)