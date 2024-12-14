from django.shortcuts import render
from rest_framework import viewsets, serializers, response, status
from personal_data.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "name", "phone_number", "email_id", "position", ]	

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_error_response(self, message, status_code):
		"""
			공통적인 에러 응답을 생성하는 메서드.
		"""
		return response.Response({"success": False, "message": message}, status=status_code)

	def get_success_response(self, message, data=None):
		"""
			공통적인 성공 응답을 생성하는 메서드.
		"""
		return response.Response({"success": True, "message": message, "data": data})

	def list(self, request, *args, **kwargs):
		email_id = request.query_params.get('email_id', None)
		queryset = self.get_queryset()
		if email_id is not None:
			queryset = queryset.filter(email_id=email_id)
			if len(queryset) != 1: 
				queryset = None
			else: 
				serializer = self.get_serializer(queryset.first())
				return response.Response({"success": True, "data": serializer.data})				
		serializer = self.get_serializer(queryset, many=True)
		return response.Response({"success": True, "data": serializer.data})

	def create(self, request, *args, **kwargs):
		username = request.data.get('username')
		email_id = request.data.get('email')
		phone_number = request.data.get('phone_number')
		emergency_contact_phone = request.data.get('emergency_contact_phone')

		# 필수 입력값 체크
		if not username or not email_id or not phone_number or not emergency_contact_phone:
			return self.get_error_response("Missing required fields", status.HTTP_400_BAD_REQUEST)

		if User.objects.filter(email_id=email_id).exists():
			return self.get_error_response("Email already exists", status.HTTP_400_BAD_REQUEST)

		try:
			# 사용자 생성 (create로 바로 저장)
			user = User.objects.create(
				username=username,
				email_id=email_id,
				phone_number=phone_number,
				emergency_contact_phone=emergency_contact_phone,
			)

			return self.get_success_response(
				"User created successfully",
				{"username": user.username, "email": user.email_id}  # email_id로 반환
			)
		
		except Exception as e:
			return self.get_error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


