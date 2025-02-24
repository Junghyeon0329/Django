from django.contrib.auth import models, hashers
from rest_framework import response, status, views, permissions, throttling

from datetime import datetime
import time

class OneSecondThrottle(throttling.UserRateThrottle): 
	rate = '1/second'	

class UserAPIView(views.APIView):
	
	""" 권한 설정 메서드. """
	def get_permissions(self):
		permission_classes = []    
		if self.request.method in ['DELETE','PUT','GET']:
			permission_classes.append(permissions.IsAuthenticated())
		return permission_classes    

	def get_throttles(self):
		throttles = super().get_throttles()
		if self.request.method == 'POST':  # POST 요청에 대해서만 1초 제한을 적용
			throttles.append(OneSecondThrottle())
		return throttles 
			
	""" 회원 탈퇴 API (자신의 계정만 삭제 가능) """
	def delete(self, request, *args, **kwargs):
		user = request.user  # 현재 로그인된 사용자
		username_to_delete = request.data.get('username', None)  # 관리자가 삭제하려는 사용자 이름

		if username_to_delete:
			# 관리자일 경우 다른 사용자의 계정을 비활성화할 수 있음
			if not user.is_staff:
				return response.Response(
					{"success": False, "message": "You are not authorized to deactivate other users."},
					status=status.HTTP_403_FORBIDDEN
				)

			try:
				# 다른 사용자의 계정을 찾아 비활성화
				target_user = models.User.objects.get(username=username_to_delete)
				target_user.is_active = False  # 계정 비활성화
				target_user.save()

				return response.Response(
					{"success": True, "message": f"User '{username_to_delete}' deactivated successfully."},
					status=status.HTTP_200_OK
				)
			except models.User.DoesNotExist:
				return response.Response(
					{"success": False, "message": "User not found."},
					status=status.HTTP_404_NOT_FOUND
				)
		else:
			# 사용자가 자기 계정을 비활성화하려는 경우
			try:
				user.is_active = False  # 계정 비활성화
				user.save()

				return response.Response(
					{"success": True, "message": "Your account has been deactivated successfully."},
					status=status.HTTP_200_OK
				)
			except Exception as e:
				return response.Response(
					{"success": False, "message": f"Error: {str(e)}."},
					status=status.HTTP_500_INTERNAL_SERVER_ERROR
				)
   
	""" 모든 유저 정보 조회 API """		 
	def get(self, request, *args, **kwargs):
		try:
			# 모든 사용자 정보 가져오기
			users = models.User.objects.all()
			
			# 사용자 정보 리스트 준비
			user_data = []
			for user in users:
				user_data.append({
					'username': user.username,
					'email': user.email,
					# 'is_superuser': user.is_superuser,
					# 'is_staff': user.is_staff,
					# 'is_active': user.is_active,
					# 'date_joined': user.date_joined,
				})

			return response.Response(
				{"success": True, "data": user_data},
				status=status.HTTP_200_OK
			)

		except Exception as e:
			return response.Response(
				{"success": False, "message": f"Error: {str(e)}."},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)