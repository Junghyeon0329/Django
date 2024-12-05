from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views

import requests
import sys
import os

class UserAPIView(views.APIView):
	# 외부 API에서 유저 정보를 가져오는 함수
	def fetch_user_info(self, email_id=None):
		try:
			sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))       
			from URLaddress import workforceURL
			if email_id:
				res = requests.get(f"http://{workforceURL['ip']}:{workforceURL['port']}/users/?email_id={email_id}")
			else :
				res = requests.get(f"http://{workforceURL['ip']}:{workforceURL['port']}/users/")
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