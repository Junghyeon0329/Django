from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views

from operation_action.usermanage import UserAPIView 
from operation_action.userlogin import LoginAPIView
from operation_action.usernotice import NoticeAPIView
from operation_action.userprofile import UserProfileUploadView
from operation_action.workforce_API import WorkforceAPIView
from operation_action.userfile import FileAPIView
from operation_action.passwordreset import PasswordResetConfirmView


from operation_action.views import chatgpt_response


''' 관리자를 추가하는 방법 : python manage.py createsuperuser '''
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginAPIView.as_view(), name='login-api'),
    path('user/', UserAPIView.as_view(), name='user-api'),    
    path('notice/', NoticeAPIView.as_view(), name='notice-api'),
    path('workforce/', WorkforceAPIView.as_view(), name='worker-api'),    
    path('file/', FileAPIView.as_view(), name='download-file'),
    path('upload/', UserProfileUploadView.as_view(), name='upload-profile'),
    path('password-reset/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('chat/', chatgpt_response, name='chatgpt_response'),
]

