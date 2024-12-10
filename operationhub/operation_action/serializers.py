# board/serializers.py
from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'author_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # POST 요청 시, 클라이언트가 author를 제공할 필요 없이 자동으로 로그인한 사용자 설정
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
