from django.shortcuts import render

from rest_framework import viewsets, serializers
from users.models import User
from custom import *
import requests
from rest_framework.response import Response

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	## 권한을 부여받은 emaili_id에 대해서 조회
	def fetch_user_info(self, email_id):
		try:
			res = requests.get(f"http://127.0.0.1:8080/users/?email_id={email_id}")
			res.raise_for_status()				
			return res.json().get("data", {})
		except requests.exceptions.RequestException as e: return {}

	def list(self, request, *args, **kwargs):
		# 기본 페이지와 페이지 크기를 정의합니다.
		page = int(request.query_params.get('page'))
		page_size = int(request.query_params.get('page_size'))

		if page == -1 and page_size == -1: users = self.queryset
		else:
			# 쿼리셋을 슬라이스하여 페이지네이션을 처리합니다.
			start = (page - 1) * page_size
			end = start + page_size
			users = self.queryset[start:end]

		# 유저 정보를 가져올 email_id 목록
		email_ids = [user.email_id for user in users]

		# 이메일 ID로 사용자 정보를 가져오기
		user_info_map = {}
		for email_id in email_ids:
			user_info_map[email_id] = self.fetch_user_info(email_id)
		
		serialized_users = []
		for user in users:
			user_info = user_info_map.get(user.email_id, {})			
			serialized_user = {
				**UserSerializer(user).data,
				'phone_number': user_info.get("phone_number", ""),
				'name': user_info.get("name", ""),
			}
			serialized_users.append(serialized_user)

		return Response({"success": True, "data": serialized_users})
