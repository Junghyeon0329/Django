from rest_framework import serializers
from notices.models import Notice

class NoticeSerializer(serializers.ModelSerializer):
	
	author = serializers.SerializerMethodField()
	
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

	def get_author(self, obj) -> str:
		if obj.author : 
			return {
				"username": obj.author.username,
				"is_admin": obj.author.is_staff,
			}
		else: return None

	def create(self, instance):		
		instance['author'] = self.context.get('request').user
		return super().create(instance)

	# def fetch_user_info(self, employee_number):
	# 	import requests
	# 	inner_server_address = 'http://127.0.0.1:5800'
	# 	try:
	# 		res = requests.get(f"{inner_server_address}/users/{employee_number}")
	# 		res.raise_for_status()  # 상태 코드 체크
	# 		return res.json().get("success", {})

	# 	except requests.exceptions.RequestException as e: return {}
			

	# def to_representation(self, instance):
	# 	representation = super().to_representation(instance)
	# 	user_info = self.fetch_user_info(instance.employee_number)
		
	# 	representation['phone_number'] = user_info.get("phone_number", "")
	# 	representation['name'] = user_info.get("name", "")  # 불필요한 따옴표 제거

	# 	return representation