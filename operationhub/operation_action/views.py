from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

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

class IsAdmin(BaseAdminPermission):
	def has_permission(self, request, view):
		# 관리자는 모든 데이터에 접근 가능
		if self.is_admin(request.user):
			return True
		return False

class UserAPIView(views.APIView):
	def get_permissions(self):
		permissions = [IsAuthenticated()]

		# GET, POST 요청에서 관리자 권한을 추가
		if self.request.method in ['GET', 'POST']:
			permissions.append(IsAdmin())
		
		# DELETE 요청에서 자기 자신만 삭제 가능하도록 처리
		elif self.request.method == 'DELETE':
			pass # 모든 로그인 사용자에게 권한 부여  

		return permissions

	## 회원탈퇴
	def delete(self, request, *args, **kwargs):
		user = request.user  # 현재 로그인된 사용자 가져오기
		try:
			# 자신의 계정만 삭제 가능하도록 처리
			user.delete()
			return response.Response({"success": True, "message": "User account deleted successfully"},
							 status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			return response.Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	
	# 비밀번호 즉시 변경 (비밀번호를 쿼리로 받음)
	def get(self, request, *args, **kwargs):
		email_id = request.query_params.get('email_id', None)
		new_password = request.query_params.get('new_password', None)  # 새 비밀번호를 쿼리로 받기

		if not email_id or not new_password:
			return response.Response({"success": False, "message": "Email and new password are required"},
							 status=status.HTTP_400_BAD_REQUEST)

		try:
			# 이메일에 해당하는 사용자 검색
			user = User.objects.get(email=email_id)
		except User.DoesNotExist:
			return response.Response({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

		# 비밀번호 업데이트 (새 비밀번호로 변경)
		user.password = make_password(new_password)  # 비밀번호를 해싱해서 저장
		user.save()

		return response.Response({"success": True, "message": "Password updated successfully"})

	# 새로운 유저 생성
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

		if User.objects.filter(username=username).exists():
			return response.Response({"success": False, "message": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

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

		