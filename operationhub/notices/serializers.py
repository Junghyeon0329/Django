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
