from django.urls import path
from django.contrib import admin

from personal_data.views import UserAuthViewSet

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("auth/", UserAuthViewSet.as_view({
        "post": "login",  # 로그인 (JWT 토큰 발급)
        "get": "verify_token",  # 토큰 검증 및 사용자 확인
        "put": "register",  # 회원가입
    })),
    
    # path("password/", UserAuthViewSet.as_view({
    #     "post": "reset_password",  # 비밀번호 초기화 (이메일 발송)
    #     "put": "change_password",  # 비밀번호 변경
    # })),

    # path("user/", UserProfileViewSet.as_view({
    #     "get": "retrieve",  # 사용자 정보 조회
    #     "put": "update",  # 사용자 정보 수정
    #     "patch": "partial_update",  # 일부 정보 수정
    #     "delete": "destroy"  # 회원 탈퇴
    # })),
]