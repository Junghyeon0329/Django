from rest_framework import serializers
from notices.models import Notice

class NoticeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notice
		fields = [
			"id",
			"title",
			"content",
			"author",
			"created_at",
			"updated_at",
		]
		read_only_fields = ['author']

	def create(self, validated_data):
		validated_data['author'] = self.context['request'].user
		return super().create(validated_data)