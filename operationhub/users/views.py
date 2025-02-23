from rest_framework import viewsets, permissions, response, status, exceptions
from rest_framework_simplejwt import authentication, tokens
from django.db import transaction
from django.contrib.auth import models, login
from django.conf import settings
import custom

class UserViewSet(viewsets.ModelViewSet):

	# get_authentication(self)에서는 self.action불가
 
	def get_permissions(self): # 유저 자격 검증
		permission = [] 
		if self.action in ['']:
			permission.append(permissions.IsAdminUser())
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
   
		# latest_password_history = PasswordHistory.objects.filter(user=user).first()	
		# if timezone.now() - latest_password_history.password_changed_at > self.password_expiry_duration:
		# 	password_expired =  True

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

	@transaction.atomic
	def register(self, request, *args, **kwargs):
	
		return response.Response({
				"success": True, "message": "test."},
				status=status.HTTP_200_OK
			)
  
	@transaction.atomic  
	def reset_password(self, request, *args, **kwargs):
	
		return response.Response({
				"success": True, "message": "test."},
				status=status.HTTP_200_OK
			)
  
	@transaction.atomic
	def change_password(self, request, *args, **kwargs):
	
		jwt_authenticator = authentication.JWTAuthentication()
		user_auth = jwt_authenticator.authenticate(self.request) # 토큰이 만료된 경우
  	
		if not user_auth: # 토큰이 없는 경우
			return response.Response({
				"success": False, "message": "Unauthorized"},
				status=status.HTTP_400_BAD_REQUEST
			)
 
		return response.Response({
				"success": True, "message": "test."},
				status=status.HTTP_200_OK
			)