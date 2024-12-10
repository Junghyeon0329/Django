# board/serializers.py
from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']  # 'author' 제외

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user  # 로그인한 사용자 설정
        return super().create(validated_data)
