from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User
from .permissions import IsAdmin, IsAdminOrOwner  # permissions.py에서 가져옴

import requests

class WorkforceAPIView(views.APIView):

	def get_permissions(self):
		permissions = [IsAuthenticated()]

		# GET/POST/DELETE 요청에서 관리자 권한 추가
		if self.request.method in ['GET', 'POST', 'DELETE']:
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


	def post_user_info(self):
		try:
			from URLaddress import workforceURL
			url = f"http://{workforceURL['ip']}:{workforceURL['port']}/users/"
			res = requests.post(url)
			res.raise_for_status()
			return res.json().get("data", {})
		except requests.exceptions.RequestException as e:
			return {}

	def post(self, request, *args, **kwargs):
		# 필수 파라미터 받기
		username = request.query_params.get('username')
		phone_number = request.query_params.get('phone_number')
		email_id = request.query_params.get('email_id')
		emergency_contact_phone = request.query_params.get('emergency_contact_phone')

		# 필수 정보가 없으면 에러 응답
		if not username or not phone_number or not email_id or not emergency_contact_phone:
			return response.JsonResponse({'error': 'Missing required fields.'}, status=400)

		# 선택적 정보 받기 (기타 정보는 request.data로 받을 수 있습니다)
		additional_info = {}
		for key, value in request.query_params.items():
			if key not in ['username', 'phone_number', 'email_id', 'emergency_contact_phone']:
				additional_info[key] = value

		# 데이터 준비 (필수 정보 + 선택적 정보)
		user_data = {
			'username': username,
			'phone_number': phone_number,
			'email_id': email_id,
			'emergency_contact_phone': emergency_contact_phone,
			**additional_info  # 선택적 정보를 추가
		}

		# post_user_info 함수에 user_data 전달
		result = self.post_user_info(user_data)

		# 결과 반환
		if 'error' in result:
			return response.JsonResponse({'error': result['error']}, status=500)

		return response.JsonResponse(result, status=200)