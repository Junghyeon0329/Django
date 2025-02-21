
from rest_framework import authentication, exceptions
import requests

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        from URLaddress import workforceURL
        url = f"http://{workforceURL['ip']}:{workforceURL['port']}/users/"
        response = requests.get(url, params={"token": token}, timeout= 5)
        
        if response.status_code != 200:
            raise exceptions.AuthenticationFailed("Invalid token")

        user_data = response.json()
        return (user_data, None)
