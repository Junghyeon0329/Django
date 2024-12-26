from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import response, status, views, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login

from datetime import datetime
import time
from .authentication import OneSecondThrottle
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
import operationhub.settings as setting

class UserAPIView(views.APIView):
	
	""" 권한 설정 메서드. """
	def get_permissions(self):
			
		permission_classes = []    
		if self.request.method in ['DELETE','PUT']:
			permission_classes.append(permissions.IsAuthenticated())
		return permission_classes    

	def get_throttles(self):
		throttles = super().get_throttles()
		if self.request.method == 'POST':  # POST 요청에 대해서만 1초 제한을 적용
			throttles.append(OneSecondThrottle())
		return throttles  

	""" 새로운 사용자 생성 API """
	def post(self, request, *args, **kwargs):
		
		# 사용자에게 필요한 나머지 정보
		email = request.data.get('email')
		password = request.data.get('password')
		is_superuser = request.data.get('is_superuser', False)
		is_staff = request.data.get('is_staff', False)

		# 필수 입력값 체크
		if not email or not password:
			return response.Response(
				{"success": False, "message": "Missing required fields."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		# email is unique (중복 확인)
		if User.objects.filter(email=email).exists():
			return response.Response(
				{"success": False, "message": "email already exists."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		# 현재 연도 + 타임스탬프 기반으로 유니크한 username 생성
		current_year = datetime.now().year
		timestamp = int(time.time())  # 현재 시간의 타임스탬프 (초 단위)
		username = f"{current_year}-{timestamp}"

		# username is unique (중복 확인)
		if User.objects.filter(username=username).exists():
			return response.Response(
				{"success": False, "message": "Username already exists."},
				status=status.HTTP_400_BAD_REQUEST
			)
   	  
		try:
			# 사용자 생성
			user = User.objects.create_user(username=username, email=email, password=password)
			user.is_superuser = is_superuser
			user.is_staff = is_superuser or is_staff  # superuser일 경우 staff도 True로 설정
			user.save()
			
			return response.Response(
					{"success": True, "message": "User created successfully."},
					status=status.HTTP_201_CREATED
				)

		except Exception as e:
			return response.Response(
					{"success": True, "message": f"{str(e)}."},
					status.HTTP_500_INTERNAL_SERVER_ERROR
				)
			
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
				target_user = User.objects.get(username=username_to_delete)
				target_user.is_active = False  # 계정 비활성화
				target_user.save()

				return response.Response(
					{"success": True, "message": f"User '{username_to_delete}' deactivated successfully."},
					status=status.HTTP_200_OK
				)
			except User.DoesNotExist:
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
	
	""" 비밀번호 변경 API (자신의 계정만 변경 가능) """
	def put(self, request, *args, **kwargs):
				
		email = request.data.get('email')
		current_password = request.data.get('current_password')  # 현재 비밀번호
		new_password = request.data.get('new_password')  # 새로운 비밀번호

		# 필수 필드 체크
		if not email or not current_password or not new_password:
			return response.Response(
				{"success": False, "message": "Missing required fields."},
				status=status.HTTP_400_BAD_REQUEST
			)

		try:
			# 사용자 객체 가져오기
			user = User.objects.get(email=email)

			# 현재 비밀번호 확인 (비밀번호가 맞는지 검증)
			if not user.check_password(current_password):
				return response.Response(
					{"success": False, "message": "Current password is incorrect."},
					status=status.HTTP_400_BAD_REQUEST
				)

			# 비밀번호가 맞다면 새로운 비밀번호로 변경
			user.password = make_password(new_password)  # 새로운 비밀번호를 해싱하여 저장
			user.save()

			return response.Response(
				{"success": True, "message": "Password updated successfully."},
				status=status.HTTP_200_OK
			)

		except User.DoesNotExist:
			return response.Response(
				{"success": False, "message": "User not found."},
				status=status.HTTP_404_NOT_FOUND
			)
				 
class LoginAPIView(views.APIView):

	""" 사용자 로그인 및 JWT 토큰 발급 """
	def post(self, request):
	
		email = request.data.get('email')
		password = request.data.get('password')

		# 필수 필드 체크
		if not email or not password:
			return response.Response(
				{"success": False, "message": "email and password are required."},
				status=status.HTTP_400_BAD_REQUEST
			)

		# 이메일로 사용자 검색
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return response.Response(
				{"success": False, "message": "No user found with this email."},
				status=status.HTTP_404_NOT_FOUND  # 사용자 없음 상태 코드
			)

		# 사용자 인증 (비밀번호 체크)
		if not user.check_password(password):
			return response.Response(
				{"success": False, "message": "Incorrect password."},
				status=status.HTTP_401_UNAUTHORIZED  # 비밀번호 불일치 상태 코드
			)

		# 비활성화된 사용자 체크
		if not user.is_active:
			return response.Response(
				{"success": False, "message": "This account is disabled."},
				status=status.HTTP_403_FORBIDDEN  # 비활성화된 계정 상태 코드
			)
	
		# 로그인 처리
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')

		# JWT 토큰 생성
		refresh = RefreshToken.for_user(user)
		access_token = str(refresh.access_token)

		return response.Response(
			{
				"success": True,
				"access": access_token,
				"refresh": str(refresh),
				"message": "Login successful."
			},
			status=status.HTTP_200_OK
		)
  
  
	""" 비밀번호 초기화 API """
	def put(self, request, *args, **kwargs):
		email = request.data.get('email')

		if not email:
			return response.Response(
				{"success": False, "message": "Missing required fields."},
				status=status.HTTP_400_BAD_REQUEST
			)

		try:
			# 사용자 객체 가져오기
			user = User.objects.get(email=email)

			# 비밀번호 초기화 토큰 생성
			token = default_token_generator.make_token(user)

			# URL 안전하게 인코딩
			uid = urlsafe_base64_encode(force_bytes(user.pk))

			# 이메일 내용 준비
			domain = get_current_site(request).domain
			# from URLaddress import front
			# domain = front['ip'] + ':' + front['port']
			reset_url = f"http://{domain}/reset-password/{uid}/{token}/"
			
			# 이메일 템플릿 렌더링
			email_subject = "비밀번호 초기화 요청"
			email_message = render_to_string('password_reset_email.html', {
				'user': user,
				'reset_url': reset_url,
			})

			try: 
				send_mail(email_subject, email_message, setting.EMAIL_HOST_USER, [email], fail_silently=False,)
			except:
				print(f"Google 보안 정책으로 2022년부터 사용 불가: {reset_url}")
				pass

			return response.Response(
				{"success": True, "message": "Password reset email sent."},
				status=status.HTTP_200_OK
			)

		except User.DoesNotExist:
			return response.Response(
				{"success": False, "message": "User not found."},
				status=status.HTTP_404_NOT_FOUND
			)