from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User

import requests

class BaseAdminPermission(BasePermission):
    def is_authenticated(self, user):
        """사용자가 인증된 상태인지 확인"""
        return user.is_authenticated

    def is_admin(self, user):
        """사용자가 관리자(Staff)인지 확인"""
        return self.is_authenticated(user) and user.is_staff

    def is_superuser(self, user):
        """사용자가 슈퍼유저인지 확인"""
        return self.is_authenticated(user) and user.is_superuser

    def is_admin_and_superuser(self, user):
        """사용자가 관리자(Staff)이고 슈퍼유저인지 확인"""
        return self.is_authenticated(user) and user.is_staff and user.is_superuser

class IsAdminOrOwner(BaseAdminPermission):
	def has_permission(self, request, view):
		# 관리자는 모든 데이터에 접근 가능
		if self.is_admin(request.user):
			return True

		# 일반 사용자는 자신의 데이터만 조회 가능
		email_id = request.query_params.get('email_id')  # URL parameter에서 email_id 추출
		if email_id and request.user.email == email_id:
			return True
		return False

class IsAdmin(BaseAdminPermission):
	def has_permission(self, request, view):
		# 관리자는 모든 데이터에 접근 가능
		if self.is_admin(request.user):
			return True
		return False

class UserAPIView(views.APIView):

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

	def post(self, request, *args, **kwargs):
     
		# 요청에서 사용자 정보 받기
		username = request.data.get('username')
		email = request.data.get('email')
		password = request.data.get('password')
		is_superuser = request.data.get('is_superuser', False)  # 기본값은 False
		is_staff = request.data.get('is_staff', False)          # 기본값은 False

		# 필수 입력값 체크
		if not username or not email or not password:
			return response.Response({"success": False, "message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

		# 이메일 중복 체크
		if User.objects.filter(email=email).exists():
			return response.Response({"success": False, "message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			# 사용자 생성
			user = User.objects.create_user(username=username, email=email, password=password)
			
			if is_superuser:
				user.is_superuser = True
				user.is_staff = True  # superuser는 staff도 True로 설정해야 함
			else:
				user.is_superuser = is_superuser
				user.is_staff = is_staff  # 프론트에서 받은 is_staff 값 그대로 사용
			
			user.save()

			return response.Response({
				"success": True,
				"message": "User created successfully",
				"data": {
					"username": user.username,
					"email": user.email,
					"is_superuser": user.is_superuser,
					"is_staff": user.is_staff
				}
			})
		
		except Exception as e:
			return response.Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		