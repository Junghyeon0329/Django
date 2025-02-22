from rest_framework import viewsets, response, status
from django.contrib.auth import models, login
from rest_framework_simplejwt import authentication, tokens, exceptions
import custom

class UserAuthViewSet(viewsets.ModelViewSet):
	queryset = models.User.objects.all()
	permission_classes = [custom.IsAllowedIP]
 
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.action in ['register']:
			throttles.append(custom.OneSecondThrottle())
		return throttles

	def login(self, request, *args, **kwargs):
    
		email = request.data.get('email')
		password = request.data.get('password')
		password_expired =  False
		
		if not email or not password:
			return response.Response(
				{"success": False, "message": "email and password are required."},
				status=status.HTTP_400_BAD_REQUEST
			)

		try: # 이메일로 사용자 검색
			user = models.User.objects.get(email=email)
		except models.User.DoesNotExist:
			return response.Response(
				{"success": False, "message": "The information received is invalid."},
				status=status.HTTP_404_NOT_FOUND
			)

		if not user.check_password(password): # 사용자 인증 (비밀번호 체크)
			return response.Response(
				{"success": False, "message": "The information received is invalid."},
				status=status.HTTP_401_UNAUTHORIZED
			)

		# 비활성화된 사용자 체크
		if not user.is_active:
			return response.Response(
				{"success": False, "message": "This account is disabled."},
				status=status.HTTP_403_FORBIDDEN
			)
   
		# latest_password_history = PasswordHistory.objects.filter(user=user).first()	
		# if timezone.now() - latest_password_history.password_changed_at > self.password_expiry_duration:
		# 	password_expired =  True

		# 로그인 처리
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')

		# JWT 토큰 생성
		refresh = tokens.RefreshToken.for_user(user)
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

	def verify_token(self, request, *args, **kwargs):

		token_key = request.GET.get("token")
		
		if not token_key:
			return response.Response(
				{"success": False, "message": "Token required"},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		authenticator = authentication.JWTAuthentication()
		
		try:
			validated_token = authenticator.get_validated_token(token_key)
			user = authenticator.get_user(validated_token)
			request.user = user
   
		except (exceptions.InvalidToken, exceptions.AuthenticationFailed):
			return response.Response(
				{"success": False, "message": "Invalid or expired token"},
				status=status.HTTP_400_BAD_REQUEST
			)

		return response.Response(
			{"success": True, "user": request.user.username}, 
			status=status.HTTP_200_OK
		)


	def register(self, request, *args, **kwargs):
		print("register")
  
	# def list(self, request, *args, **kwargs):
		# email_id = request.query_params.get('email', None)
		# queryset = self.get_queryset()
		
		# queryset = queryset.filter(permission=True)
				
		# if email_id:
		# 	queryset = queryset.filter(email_id=email_id)
		# 	if len(queryset) != 1:
		# 		queryset = None
		# 	else:
		# 		serializer = self.get_serializer(queryset.first())
		# 		return response.Response({"success": True, "data": serializer.data})

		# serializer = self.get_serializer(queryset, many=True)
		# return response.Response({"success": True, "data": serializer.data})

	# def update(self, request, *args, **kwargs):
		
	# 	error_response = self.check_and_validate_api(request)
	# 	if error_response: 
	# 		return error_response         
		
	# 	data = request.data

	# 	user_id = kwargs.get('pk')
	# 	try:
	# 		user = User.objects.get(id=user_id)
	# 	except User.DoesNotExist:
	# 		return self.get_error_response("User not found", status.HTTP_404_NOT_FOUND)

	# 	# 필드 업데이트
	# 	for field, value in data.items():
	# 		if hasattr(user, field):
	# 			setattr(user, field, value)

	# 	try:
	# 		user.save()
	# 		return self.get_success_response("User updated successfully", {"username": user.username, "email": user.email_id})
	# 	except Exception as e:
	# 		return self.get_error_response(f"Error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

	# partial_update = update


	# def create(self, request, *args, **kwargs):
	# 	data = request.data

	# 	error_response = self.check_and_validate_api(request)
	# 	if error_response: 
	# 		return error_response 

	# 	# 필수 필드 확인
	# 	required_fields = [field.name for field in User._meta.get_fields() if not field.blank and (field.default == NOT_PROVIDED)]
		
	# 	missing_fields = [field for field in required_fields if field not in data]
	# 	if missing_fields:
	# 		return response.Response(
	# 			{"success": False, "message": f"Missing required fields: {', '.join(missing_fields)}"},
	# 			status=status.HTTP_400_BAD_REQUEST
	# 		)    

	# 	# 선택적 필드 처리
	# 	extra_fields = {}
	# 	for field in User._meta.get_fields():
	# 		if field.name in data and field.name not in required_fields:
	# 			if field.name in ['permission', 'approval_data']:
	# 				continue
	# 			extra_fields[field.name] = data[field.name]
			
	# 	# email_id 중복 검사        
	# 	if User.objects.filter(email_id=data['email_id']).exists():
	# 		return response.Response(
	# 			{"success": False, "message": "Email ID already exists."},
	# 			status=status.HTTP_400_BAD_REQUEST
	# 		)
		
	# 	try:
	# 		user = User.objects.create(
	# 			username=data['username'],
	# 			email_id=data['email_id'],
	# 			**extra_fields
	# 		)
	# 		return response.Response(
	# 				{"success": True, "message": "User created successfully."},
	# 				status=status.HTTP_201_CREATED
	# 		)
	# 	except Exception as e:
	# 		return response.Response(
	# 			{"success": False, "message": f"Error occurred: {str(e)}"},
	# 			status=status.HTTP_500_INTERNAL_SERVER_ERROR
	# 		)


