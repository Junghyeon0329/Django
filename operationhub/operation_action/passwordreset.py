from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import response, status
from django.utils.encoding import force_bytes, force_str

class PasswordResetConfirmView(APIView):
            
    def put(self, request, *args, **kwargs):
        # URL에서 uid와 token 추출
        uid = kwargs.get('uid')
        token = kwargs.get('token')
        new_password = request.data.get('password')
        
        try:
            # uid와 token을 통해 사용자 정보와 유효성 검사
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            # 토큰 확인
            if default_token_generator.check_token(user, token):
                # 비밀번호 변경
                user.set_password(new_password)
                user.save()

                return response.Response(
                    {"success": True, "message": "Password reset successfully."},
                    status=status.HTTP_200_OK
                )
            else:
                return response.Response(
                    {"success": False, "message": "Invalid token."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return response.Response(
                {"success": False, "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )