from rest_framework import viewsets, serializers, response, status
from personal_data.models import User
from django.db.models.fields import NOT_PROVIDED

# 허용된 API 키 목록
ALLOWED_API_KEYS = ['127.0.0.1']

# 사용자 직렬화 클래스
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "phone_number", "email_id", "position", "emergency_contact_name", "emergency_contact_phone"]

# 사용자 뷰셋 클래스
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

    def check_api_host(self, request):
        """
            요청의 출처를 확인하는 메서드.
        """
        host = request.get_host().split(":")[0]  # 포트를 제외한 호스트 이름만 가져옴
        print(f"Request host: {host}")
        return host in ALLOWED_API_KEYS

    def check_and_validate_api(self, request):
        """
            API 요청의 출처를 검증하고, 출처가 허용되지 않으면 401 응답을 반환.
        """
        if not self.check_api_host(request):
            return self.get_error_response("Unauthorized", status.HTTP_401_UNAUTHORIZED)
        return None  # 검증이 통과하면 None을 반환

    def handle_missing_fields(self, data, required_fields):
        """
            필수 필드가 누락된 경우 에러 응답을 반환.
        """
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return self.get_error_response(f"Missing required fields: {', '.join(missing_fields)}", status.HTTP_400_BAD_REQUEST)
        return None  # 필수 필드가 모두 존재하면 None을 반환

    def handle_extra_fields(self, data, required_fields):
        """
            선택적 필드를 처리하여 반환.
        """
        extra_fields = {}
        for field in User._meta.get_fields():
            if field.name in data and field.name not in required_fields:
                extra_fields[field.name] = data[field.name]
        return extra_fields

    def create(self, request, *args, **kwargs):
        data = request.data

        # API 요청 검증
        error_response = self.check_and_validate_api(request)
        if error_response:
            return error_response

        # 필수 필드 확인
        required_fields = [field.name for field in User._meta.get_fields() if not field.blank and (field.default == NOT_PROVIDED)]
        error_response = self.handle_missing_fields(data, required_fields)
        if error_response:
            return error_response

        # 선택적 필드 처리
        extra_fields = self.handle_extra_fields(data, required_fields)
            
        # email_id 중복 검사
        
        if User.objects.filter(email_id=data['email_id']).exists():
            return self.get_error_response("Email ID already exists.", status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create(
                username=data['username'],
                email_id=data['email_id'],
                phone_number=data['phone_number'],
                emergency_contact_phone=data['emergency_contact_phone'],
                **extra_fields
            )
            return self.get_success_response("User created successfully", {"username": user.username, "email": user.email_id})
        except Exception as e:
            return self.get_error_response(f"Error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        # API 요청 검증
        error_response = self.check_and_validate_api(request)
        if error_response:
            return error_response

        email_id = request.query_params.get('email_id', None)
        queryset = self.get_queryset()
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
        data = request.data

        # API 요청 검증
        error_response = self.check_and_validate_api(request)
        if error_response:
            return error_response

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
