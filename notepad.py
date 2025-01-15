'''
    urlpatterns = [
        path("permissions/", PermissionViewSet.as_view({
            "get": "list", #모든 객체의 리스트 반환
            "post": "create" #새 객체를 생성
        })),
        path("permissions/<int:pk>/", PermissionViewSet.as_view({
            "get": "retrieve", #특정 객체를 반환
            "put": "update", # 특정 객체를 수정
            "patch": "partial_update", #특정 객체를 일부 수정
            "delete": "destroy" #특정 객체 삭제
        })),
    ]
'''


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class TokenRefreshView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 클라이언트에서 보내온 refresh token을 받음
        refresh_token = request.data.get('refresh')

        try:
            # refresh token을 사용하여 새로운 access token 생성
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({
                'access': str(access_token),
            })
        except Exception as e:
            return Response({'detail': str(e)}, status=400)


# TODO

"""
    회원가입 시 비밀번호 변경 기록 현재로 기입
    비밀번호 변경 시 기록 UPDATE

"""