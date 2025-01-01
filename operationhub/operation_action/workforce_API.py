from django.shortcuts import render
from rest_framework import response, views, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User

import requests
from requests.exceptions import RequestException, HTTPError
from .authentication import OneSecondThrottle

class WorkforceAPIView(views.APIView):

	def get_permissions(self):
		
		permissions = [IsAuthenticated]
		if self.request.method in ['POST','GET']:
			permissions.append(IsAdminUser())
		return permissions
	
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.request.method == 'POST':  # POST 요청에 대해서만 1초 제한을 적용
			throttles.append(OneSecondThrottle())
		return throttles  

	""" 새로운 인사 인원 생성 API """ 
	def post(self, request, *args, **kwargs):        
		
		email = request.data.get('email', None)
		if not email:
			return response.Response(
				{"success": False, "message": "email_id ID is required."},
				status=status.HTTP_400_BAD_REQUEST
			)

		try:
			user = User.objects.get(email=email)
			user_data = {'username' : user.username, 'email_id' : email}
			
		except User.DoesNotExist:
			return response.Response(
				{"success": False, "message": "User with this email ID does not exist."},
				status=status.HTTP_404_NOT_FOUND
			)       
		
		if not all(user_data.values()):
			return response.Response(
				{"success": False, "message": "Missing required fields."},
				status=status.HTTP_400_BAD_REQUEST
			)        
		
		# 선택적 정보 받기 (기타 정보는 request.data로 받을 수 있습니다)
		optional_fields = {key: value for key, value in request.data.items() if key not in user_data}
		user_data.update(optional_fields)
	
		# 외부 API에 유저 정보 전달 및 결과 처리
		try:
			from URLaddress import workforceURL
			url = f"http://{workforceURL['ip']}:{workforceURL['port']}/users/"

			# POST 요청 전송
			res = requests.post(url, json=user_data)
			# print("message:", res.json()['message'])
   
			# HTTP 상태 코드가 4xx, 5xx인 경우 예외 발생
			res.raise_for_status()
			
			return response.Response(
					{"success": True, "message": "User created successfully."},
					status=status.HTTP_201_CREATED
			)

		except HTTPError as http_err:
			return response.Response(
					{"success": False, "message": f"Error: {str(http_err)}."},
					status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
		  
		except RequestException as e:
			return response.Response(
					{"success": False, "message": f"Error: {str(e)}."},
					status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	""" 인사 인원 정보 요청 API """
	def get(self, request, *args, **kwargs):
		# 쿼리 파라미터에서 email 가져오기
		email = request.query_params.get('email', None)
		# URL 설정
		try:
			from URLaddress import workforceURL
			url = f"http://{workforceURL['ip']}:{workforceURL['port']}/users/"

			# GET 요청 전송
			if email:
				res = requests.get(url, params={'email': email})
			else:
				res = requests.get(url)
			# HTTP 상태 코드가 4xx, 5xx인 경우 예외 발생
			res.raise_for_status()

			# 데이터 처리
			user_info = res.json().get("data", {})

			if user_info:
				return response.Response(
				   {"success": True, "data": user_info},
					status=status.HTTP_200_OK
				)
			else:                
				return response.Response(
					{"success": False, "message": "User not found."},
					status=status.HTTP_404_NOT_FOUND
				)
				
		except HTTPError as http_err:
			return response.Response(
					{"success": False, "message": f"Error: {str(http_err)}."},
					status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)          
		  
		except RequestException as e:
			return response.Response(
					{"success": False, "message": f"Error: {str(e)}."},
					status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)