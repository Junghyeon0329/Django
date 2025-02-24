from django.urls import path
from django.contrib import admin

from operation_action import views, usermanage, userprofile
from operation_action import userfile, userpasswordreset, userchat


from notices.views import NoticeViewSet
from users.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # path('file/', userfile.FileAPIView.as_view(), name='download-file'),
    # path('upload/', userprofile.UserProfileUploadView.as_view(), name='upload-profile'),
    # path('password-reset/<uid>/<token>/', userpasswordreset.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('workforce/', workforce_API.WorkforceAPIView.as_view(), name='worker-api'), 
    # path('chatgpt/', views.chatgpt_response, name='chatgpt_response'),
    # path('chat/', userchat.ChatHistoryAPIView.as_view(), name='chat-history'),    
    # path('user/', usermanage.UserAPIView.as_view(), name='user-api'),
    # path('login/', views.homepage_login),
    
    path("login/", UserViewSet.as_view({
        "post": "login",  # 로그인 (JWT 토큰 발급)
        "put": "register",  # 회원가입
    })),
    
    path("password/", UserViewSet.as_view({
        "post": "reset_password",  # 비밀번호 초기화
        "patch" : "reset_password_url", # 비밀번호 초기화(url)
        "put": "change_password",  # 비밀번호 변경
    })),
    
    path("user/", UserViewSet.as_view({
        "get": "retrieve",  # 사용자 정보 조회
        "put": "update",  # 사용자 정보 수정
        "patch": "partial_update",  # 일부 정보 수정
        "delete": "destroy"  # 회원 탈퇴
    })),
    
    path("notice/", NoticeViewSet.as_view({
        "get": "list", # 공지사항 조회
        "post": "create", # 공지사항 생성
        "patch": "partial_update", # 공지사항 수정
        "delete": "destroy", # 공지사항 삭제
    })),
    
]

