from django.urls import path
from django.contrib import admin

from operation_action import usermanage, userlogin, userprofile
from operation_action import workforce_API, userfile, userpasswordreset, userchat
from operation_action.views import chatgpt_response

from notices.views import NoticeViewSet

''' 관리자를 추가하는 방법 : python manage.py createsuperuser '''
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('file/', userfile.FileAPIView.as_view(), name='download-file'),
    path('upload/', userprofile.UserProfileUploadView.as_view(), name='upload-profile'),
    path('password-reset/<uid>/<token>/', userpasswordreset.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('workforce/', workforce_API.WorkforceAPIView.as_view(), name='worker-api'),    
    path('chatgpt/', chatgpt_response, name='chatgpt_response'),
    path('chat/', userchat.ChatHistoryAPIView.as_view(), name='chat-history'),    
    
    path('login/', userlogin.LoginAPIView.as_view(), name='login-api'),
    path('user/', usermanage.UserAPIView.as_view(), name='user-api'),    
    
    path("notice", NoticeViewSet.as_view({
        "get": "list",
        "post": "create",
        "patch": "partial_update",
        "delete": "destroy",
    })),
    
]

