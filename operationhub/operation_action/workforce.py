from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User
from .permissions import IsAdmin, IsAdminOrOwner  # permissions.py에서 가져옴

import requests

class WorkforceAPIView(views.APIView):

	def get_permissions(self):
		permissions = [IsAuthenticated()]

		# GET 요청: IsAdminOrOwner 권한 추가
		if self.request.method == 'GET':
			permissions.append(IsAdminOrOwner())
		
		# POST 요청: IsAdmin 권한 추가
		elif self.request.method == 'POST':
			permissions.append(IsAdmin())
		
		return permissions

 	# 외부 API에서 유저 정보를 가져오는 함수
	def fetch_user_info(self, email_id=None):
		try:
			from URLaddress import workforceURL
			url = f"http://{workforceURL['ip']}:{workforceURL['port']}/users/"
			if email_id:
				url += f"?email_id={email_id}"
			res = requests.get(url)
			res.raise_for_status()                
			return res.json().get("data", {})
		except requests.exceptions.RequestException as e:
			return {}

	def get(self, request, *args, **kwargs):
	 
		# 쿼리 파라미터에서 이메일 ID를 가져옵니다.
		email_id = request.query_params.get('email_id', None)
		user_info = self.fetch_user_info(email_id)
  
		if user_info:
			return response.Response({"success": True, "data": user_info})
		else:
			if email_id:
				return response.Response({"success": False, "message": "User not found"}, status=404)
			else:
				return response.Response({"success": True, "data": []})
