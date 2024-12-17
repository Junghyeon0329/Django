from rest_framework import viewsets, serializers, response, status, throttling
from personal_data.models import User
from django.db.models.fields import NOT_PROVIDED

# 허용된 API 키 목록
ALLOWED_API_KEYS = ['165.132.105.29']

class OneSecondThrottle(throttling.UserRateThrottle): rate = '1/second'	

# 사용자 직렬화 클래스
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "phone_number", "email_id", "position", "emergency_contact_name", "emergency_contact_phone"]

# 사용자 뷰셋 클래스
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	""" 요청 출처 확인 메서드. """
	def check_and_validate_api(self, request):
		host = request.get_host().split(":")[0]
		if host not in ALLOWED_API_KEYS:
			return response.Response(
				{"success": False, "message": "Unauthorized"},
				status=status.HTTP_401_UNAUTHORIZED
			)
		return None  
	
	"""API 1초에 1번으로 제한 : 429_TOO_MANY_REQUESTS"""
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.action == 'create':
			throttles.append(OneSecondThrottle())
		return throttles

	def create(self, request, *args, **kwargs):
		data = request.data

		error_response = self.check_and_validate_api(request)
		if error_response: 
			return error_response 

		print("(1)")
		print(User._meta.get_fields())
  
		# 필수 필드 확인
		required_fields = [field.name for field in User._meta.get_fields() if not field.blank and (field.default == NOT_PROVIDED)]
		
		missing_fields = [field for field in required_fields if field not in data]
		if missing_fields:
			return response.Response(
				{"success": False, "message": f"Missing required fields: {', '.join(missing_fields)}"},
				status=status.HTTP_400_BAD_REQUEST
			)    

		# 선택적 필드 처리
		extra_fields = {}
		for field in User._meta.get_fields():
			if field.name in data and field.name not in required_fields:
				if field.name in ['permission', 'approval_data']:
					continue
				extra_fields[field.name] = data[field.name]
			
		# email_id 중복 검사        
		if User.objects.filter(email_id=data['email_id']).exists():
			return response.Response(
				{"success": False, "message": "Email ID already exists."},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		try:
			user = User.objects.create(
				username=data['username'],
				email_id=data['email_id'],
				**extra_fields
			)
			return response.Response(
					{"success": True, "message": "User created successfully."},
					status=status.HTTP_201_CREATED
			)
		except Exception as e:
			return response.Response(
				{"success": False, "message": f"Error occurred: {str(e)}"},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

	def list(self, request, *args, **kwargs):

		error_response = self.check_and_validate_api(request)
		if error_response: 
			return error_response 

		email_id = request.query_params.get('email', None)
		queryset = self.get_queryset()
		
		queryset = queryset.filter(permission=True)
				
		if email_id:
			queryset = queryset.filter(email_id=email_id)
			if len(queryset) != 1:
				queryset = None
			else:
				serializer = self.get_serializer(queryset.first())
				return response.Response({"success": True, "data": serializer.data})

		serializer = self.get_serializer(queryset, many=True)
		return response.Response({"success": True, "data": serializer.data})

	def update(self, request, *args, **kwargs):
		
		error_response = self.check_and_validate_api(request)
		if error_response: 
			return error_response         
		
		data = request.data

		user_id = kwargs.get('pk')
		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return self.get_error_response("User not found", status.HTTP_404_NOT_FOUND)

		# 필드 업데이트
		for field, value in data.items():
			if hasattr(user, field):
				setattr(user, field, value)

		try:
			user.save()
			return self.get_success_response("User updated successfully", {"username": user.username, "email": user.email_id})
		except Exception as e:
			return self.get_error_response(f"Error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

	partial_update = update





