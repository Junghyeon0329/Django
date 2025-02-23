
from rest_framework import authentication, exceptions, response, status
import requests

class JWTAuthentication2(authentication.BaseAuthentication):
    
    """ 공통 예외 처리 """
    def _handle_request_exception(self, exception):
        if isinstance(exception, requests.Timeout):
            return response.Response({
                "success": False, "message": "Request timedout."},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exception, requests.RequestException):
            return response.Response({
                "success": False, "message": "Communication error."},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exception, ValueError):
            return response.Response({
                "success": False, "message": "Format error."},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return response.Response({
                "success": False, "message": "Unknown error."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    """ 로그인 (JWT 토큰 발급) """
    def login(self, request):
        try:
            from URLaddress import workforceURL
            url = f"http://{workforceURL['ip']}:{workforceURL['port']}/auth/"
            res = requests.post(url, data=request.data, timeout=5)
            
        except (requests.Timeout, requests.RequestException, ValueError) as e:
            return self._handle_request_exception(e)

        if res.status_code != 200:
            return response.Response({
                "success": False, "message": res.json().get('message')},
                status=res.status_code
            )
    
        return response.Response({
                "success": True, "message": res.json().get('message')},
                status=res.status_code
            )
    
    """ 토큰 검증 및 사용자 확인 """
    def verify_token(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return response.Response({
                "success": False, "message": 'Lack of information.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            from URLaddress import workforceURL
            url = f"http://{workforceURL['ip']}:{workforceURL['port']}/auth/"
            res = requests.get(url, headers={"Authorization": f"{auth_header}"}, timeout=5)
            
        except (requests.Timeout, requests.RequestException, ValueError) as e:
            return self._handle_request_exception(e)

        if res.status_code != 200:
            return response.Response({
                "success": False, "message": res.json().get('message')},
                status=res.status_code
            )
            
        return response.Response({
                "success": True, "message": res.json().get('message')},
                status=res.status_code
            )
    
    
