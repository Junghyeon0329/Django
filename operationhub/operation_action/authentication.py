from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from rest_framework import throttling 

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email) # 이메일을 통해 사용자 찾기
            if user.check_password(password): # 비밀번호 검증
                return user
        except User.DoesNotExist:
            return None

class OneSecondThrottle(throttling.UserRateThrottle): 
    rate = '1/second'