
from rest_framework import authentication, exceptions
import requests

class JWTAuthentication(authentication.BaseAuthentication):
    
    """ 공통 예외 처리 """
    def _handle_request_exception(self, exception):
        if isinstance(exception, requests.Timeout):
            return {
                "success": False,
                "message": "서버 요청 시간이 초과되었습니다."
            }
        elif isinstance(exception, requests.RequestException):
            return {
                "success": False,
                "message": "서버와의 통신 중 오류가 발생했습니다."
            }
        elif isinstance(exception, ValueError):
            return {
                "success": False,
                "message": "서버 응답이 올바른 형식이 아닙니다."
            }
        else:
            return {
                "success": False,
                "message": "알 수 없는 오류가 발생했습니다."
            }
        
    """ 로그인 (JWT 토큰 발급) """
    def login(self, request):
        try:
            from URLaddress import workforceURL
            url = f"http://{workforceURL['ip']}:{workforceURL['port']}/auth/"
            response = requests.post(url, data=request.data, timeout=5)
            
        except (requests.Timeout, requests.RequestException, ValueError) as e:
            self._handle_request_exception(e)

        if response.status_code != 200:
            return {
                "success": False,
                "message": f"오류: {response.status_code}: {response.json().get('message', '알 수 없는 오류')}"
            }
    
        return response
    
    """ 토큰 검증 및 사용자 확인 """
    def verify_token(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {
                "success": False,
                "message": "Authorization header missing or malformed."
            }
        token = auth_header.split(" ")[1]                
        try:
            from URLaddress import workforceURL
            url = f"http://{workforceURL['ip']}:{workforceURL['port']}/auth/"
            response = requests.get(url, params={"token": token}, timeout=5)
        except (requests.Timeout, requests.RequestException, ValueError) as e:
            self._handle_request_exception(e)

        if response.status_code != 200:
            return {
                "success": False,
                "message": f"오류: {response.status_code}: {response.json().get('message', '알 수 없는 오류')}"
            }
        
        return {
            "success": True,
            "data": response.json()
        }
    
    
