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

	# def create(self, instance):		
	# 	instance['author'] = self.context.get('user')
	# 	return super().create(instance)