from django.urls import path
from django.contrib import admin

from operation_action import views, usermanage, userlogin, userprofile
from operation_action import userfile, userpasswordreset, userchat


from notices.views import NoticeViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('file/', userfile.FileAPIView.as_view(), name='download-file'),
    path('upload/', userprofile.UserProfileUploadView.as_view(), name='upload-profile'),
    path('password-reset/<uid>/<token>/', userpasswordreset.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('workforce/', workforce_API.WorkforceAPIView.as_view(), name='worker-api'),    
    path('chatgpt/', views.chatgpt_response, name='chatgpt_response'),
    path('chat/', userchat.ChatHistoryAPIView.as_view(), name='chat-history'),    
    
    # path('login/', userlogin.LoginAPIView.as_view(), name='login-api'),
    # path('user/', usermanage.UserAPIView.as_view(), name='user-api'),
    
    path('login/', views.homepage_login),
    path("notice/", NoticeViewSet.as_view({
        "get": "list", # 공지사항 조회
        "post": "create", # 공지사항 생성
        "patch": "partial_update", # 공지사항 수정
        "delete": "destroy", # 공지사항 삭제
    })),
    
]

