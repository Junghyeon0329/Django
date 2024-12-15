from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import response, status, views
from rest_framework.permissions import IsAuthenticated

class UserAPIView(views.APIView):

    def get_permissions(self):
        """
			권한 설정 메서드.
			GET/POST 요청에 IsAdmin 권한을 추가하고, DELETE 요청에 자기 자신만 삭제 가능하도록 설정.
        """
        permissions = [IsAuthenticated()]

        # GET/POST 요청에서 관리자 권한 추가
        if self.request.method in ['GET', 'POST']:
            permissions.append(IsAdmin())
        
        # DELETE 요청에서 자기 자신만 삭제 가능하도록 처리
        elif self.request.method == 'DELETE':
            pass  # 모든 로그인 사용자에게 권한 부여  

        return permissions

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

    def get(self, request, *args, **kwargs):
        """
        	비밀번호 변경 API (쿼리로 받은 이메일과 새 비밀번호로 비밀번호 변경)
        """
        email = request.query_params.get('email_id')
        new_password = request.query_params.get('new_password')

        if not email or not new_password:
            return self.get_error_response("Email and new password are required", status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.get_error_response("User not found", status.HTTP_404_NOT_FOUND)

        user.password = make_password(new_password)
        user.save()

        return self.get_success_response("Password updated successfully")

    def post(self, request, *args, **kwargs):
        """
        	새로운 사용자 생성 API
        """
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_superuser = request.data.get('is_superuser', False)
        is_staff = request.data.get('is_staff', False)

        # 필수 입력값 체크
        if not username or not email or not password:
            return self.get_error_response("Missing required fields", status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return self.get_error_response("Email already exists", status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return self.get_error_response("Username already exists", status.HTTP_400_BAD_REQUEST)

        try:
            # 사용자 생성
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_superuser = is_superuser
            user.is_staff = is_superuser or is_staff  # superuser일 경우 staff도 True로 설정

            user.save()

            return self.get_success_response(
                "User created successfully",
                {"username": user.username, "email": user.email, "is_superuser": user.is_superuser, "is_staff": user.is_staff}
            )
        
        except Exception as e:
            return self.get_error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        """
        	회원 탈퇴 API (자신의 계정만 삭제 가능)
        """
        user = request.user  # 현재 로그인된 사용자

        try:
            user.delete()
            return self.get_success_response("User account deleted successfully")
        except Exception as e:
            return self.get_error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
