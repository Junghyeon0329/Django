from django.shortcuts import render

from rest_framework import viewsets, serializers
from users.models import User
from custom import *
import requests

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'

	def fetch_user_info(self, email_id):
		try:
			res = requests.get(f"http://127.0.0.1:8080/users/?email_id={email_id}")
			res.raise_for_status()	
			return res.json().get("data", {})
		except requests.exceptions.RequestException as e: return {}

	def to_representation(self, instance):
		representation = super().to_representation(instance)		
		user_info = self.fetch_user_info(instance.email_id)
		if user_info != []:
			representation['phone_number'] = user_info.get("phone_number", "")
			representation['name'] = user_info.get("name", "")  # 불필요한 따옴표 제거
		else: 
			representation['phone_number'] = ""
			representation['name'] = ""
		return representation

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer	
	# pagination_class = CustomPagination

