
from rest_framework import response, status, views, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, models, tokens
from django.utils import timezone, http, encoding
from django.template.loader import render_to_string
from .models import PasswordHistory
from datetime import timedelta

class LoginAPIView(views.APIView):
	
	authentication_classes = []
	permission_classes = [permissions.AllowAny]
	password_expiry_duration = timedelta(days=30)
	
	""" 사용자 로그인 및 JWT 토큰 발급 """
	def post(self, request):
				
		email = request.data.get('email')
		password = request.data.get('password')
		password_expired =  False
		
		# 필수 필드 체크
		if not email or not password:
			return response.Response(
				{"success": False, "message": "email and password are required."},
				status=status.HTTP_400_BAD_REQUEST
			)

		# 이메일로 사용자 검색
		try:
			user = models.User.objects.get(email=email)
		except models.User.DoesNotExist:
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
   
		latest_password_history = PasswordHistory.objects.filter(user=user).first()	
		if timezone.now() - latest_password_history.password_changed_at > self.password_expiry_duration:
			password_expired =  True

		# 로그인 처리
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')

		# JWT 토큰 생성
		refresh = RefreshToken.for_user(user)
		access_token = str(refresh.access_token)

		staff_or_superuser = user.is_staff or user.is_superuser
  
		return response.Response(
			{
				"success": True,
				"access": access_token,
				"refresh": str(refresh),
				"user":{
					"username": user.username,
	 				"email": user.email,
					"joinedDate" : user.date_joined,
					"staff": staff_or_superuser,
					"password_expired": password_expired 
				},
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
			user = models.User.objects.get(email=email)

			# 비밀번호 초기화 토큰 생성
			token = tokens.default_token_generator.make_token(user)

			# URL 안전하게 인코딩
			uid = http.urlsafe_base64_encode(encoding.force_bytes(user.pk))

			# 이메일 내용 준비
			# domain = get_current_site(request).domain
			from URLaddress import front
			domain = front['ip'] + ':' + front['port']
			reset_url = f"http://{domain}/reset-password/{uid}/{token}/"
			
			# 이메일 템플릿 렌더링
			email_subject = "비밀번호 초기화 요청"
			email_message = render_to_string('password_reset_email.html', {
				'user': user,
				'reset_url': reset_url,
			})

			print(f"Google 보안 정책으로 2022년부터 사용 불가: {reset_url}")

			return response.Response(
				{"success": True, "message": "Password reset email sent."},
				status=status.HTTP_200_OK
			)

		except models.User.DoesNotExist:
			return response.Response(
				{"success": False, "message": "User not found."},
				status=status.HTTP_404_NOT_FOUND
			)