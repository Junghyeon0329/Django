from django.urls import path
from django.contrib import admin

from operation_action import views, usermanage, userlogin, userprofile
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
    # path('login/', userlogin.LoginAPIView.as_view(), name='login-api'),
    # path('user/', usermanage.UserAPIView.as_view(), name='user-api'),
    # path('login/', views.homepage_login),
    
    path("login/", UserViewSet.as_view({
        "post": "login",  # 로그인 (JWT 토큰 발급)
        "put": "register",  # 회원가입
    })),
    
    path("password/", UserViewSet.as_view({
        "post": "reset_password",  # 비밀번호 초기화 (이메일 발송)
        "put": "change_password",  # 비밀번호 변경
    })),
    
    path("notice/", NoticeViewSet.as_view({
        "get": "list", # 공지사항 조회
        "post": "create", # 공지사항 생성
        "patch": "partial_update", # 공지사항 수정
        "delete": "destroy", # 공지사항 삭제
    })),
    
]

