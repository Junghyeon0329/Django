from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import status, viewsets, serializers, response, views
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 세션에 사용자 정보를 저장 (일반적으로 세션 기반 로그인)
            login(request, user)

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return response.Response({
                'access_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return response.Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
