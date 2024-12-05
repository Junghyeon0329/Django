from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views

import requests
import sys
import os

class UserAPIView(views.APIView):
	# 외부 API에서 유저 정보를 가져오는 함수
	def fetch_user_info(self, email_id):
		try:
			sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))       
			from URLaddress import workforceURL
			res = requests.get(f"http://{workforceURL['ip']}:{workforceURL['port']}/users/?email_id={email_id}")
			res.raise_for_status()                
			return res.json().get("data", {})
		except requests.exceptions.RequestException as e:
			return {}

	def get(self, request, *args, **kwargs):
		# 쿼리 파라미터에서 이메일 ID를 가져옵니다.
		email_id = request.query_params.get('email_id', None)
		
		# 외부 API로부터 유저 정보를 가져오기
		if email_id:
			user_info = self.fetch_user_info(email_id)
			if user_info:
				return response.Response({"success": True, "data": user_info})
			else:
				return response.Response({"success": False, "message": "User not found"}, status=404)

		return response.Response({"success": True, "data": []})