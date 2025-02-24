from rest_framework import viewsets, permissions, response, status
from rest_framework_simplejwt import authentication, tokens
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import models, login, hashers
from django.conf import settings
from django.utils import timezone, encoding, http
from datetime import timedelta, datetime
from .models import PasswordHistory
import time
import custom

class UserViewSet(viewsets.ModelViewSet):
	password_expiry_duration = timedelta(days=30)
	# get_authentication(self)에서는 self.action불가
 
	def get_permissions(self): # 유저 자격 검증
		permission = [] 
		if self.action in ['']:
			permission.append(permissions.IsAdminUser())
   
		elif self.action in ['change_password','withdrawal','retrieve']:
			permission.append(permissions.IsAuthenticated())
			
		return permission

	def get_throttles(self): # 횟수, 빈도 제한
		throttles = super().get_throttles()
		if self.action in ['register', 'reset_password', 'change_password']:
			throttles.append(custom.OneSecondThrottle())			
		return throttles

	""" 계정 로그인 """
	def login(self, request, *args, **kwargs):
		email = request.data.get('email')
		password = request.data.get('password')
		password_expired =  False
  
		if not email or not password:
			return response.Response({
				"success": False, "message": "Lack of information."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		try:
			user = models.User.objects.get(email=email)
		except models.User.DoesNotExist:
			return response.Response({
				"success": False, "message": "Information error."},
				status=status.HTTP_404_NOT_FOUND
			)

		if not user.check_password(password):
			return response.Response({
				"success": False, "message": "Information error."},
				status=status.HTTP_401_UNAUTHORIZED
			)

		if not user.is_active:
			return response.Response({
				"success": False, "message": "Invalid account."},
				status=status.HTTP_403_FORBIDDEN
			)

		## 비밀번호 만료
		latest_pw = PasswordHistory.objects.filter(user=user).first()
		if timezone.now()- latest_pw.pw_changed_at > self.password_expiry_duration:
			password_expired =  True

		login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

		refresh = tokens.RefreshToken.for_user(user)
		access_token = str(refresh.access_token)
   
		staff_or_superuser = user.is_staff or user.is_superuser
  
		return response.Response({
			"success": True, 
			"message":{
				"access": access_token,
				"refresh": str(refresh),
				"user":{
					"username": user.username,
					"email": user.email,
					"joinedDate" : user.date_joined,
					"staff": staff_or_superuser,
					"password_expired": password_expired 
				},
			}},status=status.HTTP_200_OK)
  
	""" 계정 회원가입 """
	@transaction.atomic
	def register(self, request, *args, **kwargs):
	 
		email = request.data.get('email')
		password = request.data.get('password')

		if not email or not password:
			return response.Response({
				"success": False, "message": "Lack of information."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		if models.User.objects.filter(email=email).exists():
			return response.Response({
				"success": False, "message": "Duplicated email"},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		## TODO 사원정보를 확인하는 방식으로 인사팀에 등록되야 하는 유저인지 아닌지 구분
		username = f"{datetime.now().year}-{int(time.time())}" # unique username(사원번호)
		 
		try:
			user = models.User.objects.create_user(username=username, email=email, password=password)
			user.save()
			
			PasswordHistory.objects.create(user=user)
			
			## TODO 인사관리팀에 회원가입한 유저 알려주기
   
			return response.Response({
					"success": True, "message": "User created successfully."},
					status=status.HTTP_201_CREATED
				)

		except Exception as e:
			return response.Response({
					"success": False, "message": f"{str(e)}."},
					status.HTTP_500_INTERNAL_SERVER_ERROR
				)
   
	""" 계정 회원탈퇴 """
	@transaction.atomic
	def withdrawal(self, request, *args, **kwargs):

		# 토큰을 직접 검사하려고 할때 적용
		# jwt_authenticator = authentication.JWTAuthentication()
		# user_auth = jwt_authenticator.authenticate(request)
  
		# if not user_auth:
		# 	return response.Response({
		# 		"success": False, "message": "Unauthorized"},
		# 		status=status.HTTP_400_BAD_REQUEST
		# 	)

		user = models.User.objects.get(username=request.user)
		try:
			# TODO 인사관리팀에 해당 사원의 회원탈퇴 확인
			user.is_active = False
			user.save()

			return response.Response({
					"success": True, "message": "Deactivated successfully."},
					status=status.HTTP_200_OK
				)
   
		except Exception as e:
			return response.Response({
					"success": False, "message": f"{str(e)}."},
					status=status.HTTP_400_BAD_REQUEST
				)
 
	""" 비밀번호 초기화 """
	@transaction.atomic  
	def reset_password(self, request, *args, **kwargs):
		email = request.data.get('email')
		username = request.data.get('username')
  
		if not email or not username:
			return response.Response({
				"success": False, "message": "Lack of information."},
				status=status.HTTP_400_BAD_REQUEST
			)

		try:
			## 해당 조건에 맞는 객체가 하나인 경우만 정상적으로 작동
			user = models.User.objects.get(Q(email=email) & Q(username=username))

			PasswordHistory.objects.update_or_create(
				user=user, 
				defaults={'pw_changed_at': timezone.now()}
			)

			user.set_password('test')
			user.save()

			## TODO 비밀번호 초기화 url 생성(URL 이메일로 전송)
			# from django.utils import http, encoding
			# token = tokens.default_token_generator.make_token(user)
			# uid = http.urlsafe_base64_encode(encoding.force_bytes(user.pk))
			# from URLaddress import front
			# domain = front['ip'] + ':' + front['port']
			# reset_url = f"http://{domain}/reset-password/{uid}/{token}/"   

		except Exception as e:
			return response.Response({
					"success": False, "message": f"{str(e)}."},
					status=status.HTTP_400_BAD_REQUEST
				)

		return response.Response({
				"success": True, "message": "Password reset successfully."},
				status=status.HTTP_200_OK
			)

	""" 비밀번호 초기화(url) """
	@transaction.atomic  
	def reset_password_url(self, request, *args, **kwargs):
		uid = kwargs.get('uid')
		token = kwargs.get('token')
		new_password = request.data.get('password')
  
		if not uid or not token or not new_password:
			return response.Response({
				"success": False, "message": "Lack of information."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		try:
			user_id = encoding.force_str(http.urlsafe_base64_decode(uid))
			user = models.User.objects.get(pk=user_id)

			
			if tokens.default_token_generator.check_token(user, token):
	   
				PasswordHistory.objects.update_or_create(
					user=user, 
					defaults={'pw_changed_at': timezone.now()}
				)
	   
				user.set_password(new_password)
				user.save()

				return response.Response({
						"success": True, "message": "Password reset successfully."},
						status=status.HTTP_200_OK
					)
			else:
				return response.Response({
					"success": False, "message": "Invalid token."},
					status=status.HTTP_400_BAD_REQUEST
				)
	
		except Exception as e:
			return response.Response({
					"success": False, "message": f"{str(e)}."},
					status=status.HTTP_400_BAD_REQUEST
				)
   
	""" 비밀번호 변경 """
	@transaction.atomic
	def change_password(self, request, *args, **kwargs):
		
		current_password = request.data.get('current_password')
		new_password = request.data.get('new_password')

		if not current_password or not new_password:
			return response.Response({
				"success": False, "message": "Lack of information."},
				status=status.HTTP_400_BAD_REQUEST
			)
		try:
			user = models.User.objects.get(username=request.user)
			if not user.check_password(current_password):
				return response.Response({
					"success": False, "message": "Unauthorized(Password)"},
					status=status.HTTP_400_BAD_REQUEST
				)
			
			PasswordHistory.objects.update_or_create(
				user=user, 
				defaults={'pw_changed_at': timezone.now()}
			)
			
			user.password = hashers.make_password(new_password)
			user.save()

			return response.Response({
				"success": True, "message": "Password updated successfully."},
				status=status.HTTP_200_OK
			)

		except Exception as e:
			return response.Response({
					"success": False, "message": f"{str(e)}."},
					status.HTTP_500_INTERNAL_SERVER_ERROR
				)
 
	""" 사용자 정보 조회 """
	def retrieve(self, request, *args, **kwargs):
     
		try:
			users = models.User.objects.all()
			
			user_data = []
			for user in users:
				user_data.append({'username': user.username,'email': user.email})

			return response.Response({
				"success": True, "message":{"data": user_data}},
                status=status.HTTP_200_OK
            )

		except Exception as e:
			return response.Response({
					"success": False, "message": f"{str(e)}."},
					status.HTTP_500_INTERNAL_SERVER_ERROR
				)


