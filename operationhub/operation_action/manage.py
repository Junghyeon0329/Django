from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import response, status, views, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

class UserAPIView(views.APIView):
    
    """ 권한 설정 메서드. """
    def get_permissions(self):
            
        permission_classes = []    
        if self.request.method in ['DELETE','PUT']:
            permission_classes.append(permissions.IsAuthenticated())
        return permission_classes    

    """ 새로운 사용자 생성 API """
    def post(self, request, *args, **kwargs):
            
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_superuser = request.data.get('is_superuser', False)
        is_staff = request.data.get('is_staff', False)

        # 필수 입력값 체크
        if not username or not email or not password:
            return response.Response(
                    {"success": False, "message": "Missing required fields."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        # username is unique
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
                
        username = request.data.get('username')  # 사용자 아이디
        current_password = request.data.get('current_password')  # 현재 비밀번호
        new_password = request.data.get('new_password')  # 새로운 비밀번호

        # 필수 필드 체크
        if not username or not current_password or not new_password:
            return response.Response(
                {"success": False, "message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 사용자 객체 가져오기
            user = User.objects.get(username=username)

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
    
        username = request.data.get('username')
        password = request.data.get('password')

        # 필수 필드 체크
        if not username or not password:
            return response.Response(
                {"success": False, "message": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 사용자 인증
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

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
        else:
            return response.Response(
                {"success": False, "message": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )