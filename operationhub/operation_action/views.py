from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views
from rest_framework.permissions import IsAuthenticated, BasePermission

import requests
import sys
import os

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        # 인증된 사용자만 접근 가능
        if not request.user.is_authenticated: 
            return False

        # 관리자는 모든 데이터에 접근 가능
        if request.user.is_staff:
            return True

        # 일반 사용자는 자신의 데이터만 조회 가능
        email_id = request.query_params.get('email_id')  # URL parameter에서 email_id 추출
        if email_id and request.user.email == email_id:
            return True

        # 나머지는 접근 불가
        return False

class UserAPIView(views.APIView):
	# 외부 API에서 유저 정보를 가져오는 함수
	def fetch_user_info(self, email_id=None):
		try:
			from URLaddress import workforceURL
			if email_id:
				res = requests.get(f"http://{workforceURL['ip']}:{workforceURL['port']}/users/?email_id={email_id}")
			else :
				res = requests.get(f"http://{workforceURL['ip']}:{workforceURL['port']}/users/")
			res.raise_for_status()                
			return res.json().get("data", {})
		except requests.exceptions.RequestException as e:
			return {}
	
	permission_classes = [IsAuthenticated, IsAdminOrOwner]
 
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