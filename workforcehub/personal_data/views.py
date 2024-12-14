from rest_framework import viewsets, serializers, response, status
from personal_data.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import NOT_PROVIDED

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username", "phone_number", "email_id", "position", "emergency_contact_name", "emergency_contact_phone"]


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

	## 사원 등록
	def create(self, request, *args, **kwargs):
		data = request.data

		required_fields = [
			field.name 
			for field in User._meta.get_fields()
			if not field.blank and (field.default == NOT_PROVIDED)
		]
		
		# 입력 데이터에서 필수 필드가 없는지 체크
		missing_fields = [field for field in required_fields if field not in data]

		if missing_fields:
			return self.get_error_response(f"Missing required fields: {', '.join(missing_fields)}", status.HTTP_400_BAD_REQUEST)

		# 선택적 필드 처리: 값이 있을 경우에만 반영
		extra_fields = {}
		for field in User._meta.get_fields():
			field_name = field.name

			# 필수 필드가 아니면서 데이터가 있으면 extra_fields에 추가
			if field_name in data and field_name not in required_fields:
				extra_fields[field_name] = data[field_name]

		try:
			# 사용자 생성 (필수 필드와 선택적 필드 반영)
			user = User.objects.create(
				username=data['username'], 
				email_id=data['email_id'], 
				phone_number=data['phone_number'],  
				emergency_contact_phone=data['emergency_contact_phone'],  
				**extra_fields  # 선택적 필드만 포함
			)

			return self.get_success_response(
				"User created successfully",
				{"username": user.username, "email": user.email_id}
			)

		except Exception as e:
			return self.get_error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

	## 사원 검색
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

	## 사원 정보 변경
	def update(self, request, *args, **kwargs):
		data = request.data

		# 요청된 'id'로 사용자 객체를 찾습니다.
		user_id = kwargs.get('pk')
		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return self.get_error_response("User not found", status.HTTP_404_NOT_FOUND)

		# 전달된 데이터에서 사용자가 수정하려는 항목을 확인하고 업데이트
		for field, value in data.items():
			if hasattr(user, field):  # 해당 필드가 모델에 있는지 확인
				setattr(user, field, value)

		try:
			user.save()  # 사용자 객체 저장
			return self.get_success_response(
				"User updated successfully",
				{"username": user.username, "email": user.email_id}
			)
		except Exception as e:
			return self.get_error_response(f"Error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

	def partial_update(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)  # update 메서드를 재사용