from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User

import requests
from requests.exceptions import RequestException, HTTPError

class WorkforceAPIView(views.APIView):

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method in ['GET', 'POST', 'DELETE']:
            permissions.append(IsAdmin())
        return permissions

    def make_api_request(self, method, endpoint, data=None):
 
        try:
            from URLaddress import workforceURL
            url = f"http://{workforceURL['ip']}:{workforceURL['port']}/{endpoint}"

            if method == 'GET':
                # GET 요청일 경우 쿼리 파라미터로 데이터 전달
                response = requests.get(url, params=data)  # params는 URL에 쿼리 파라미터를 추가하는 방식
            elif method == 'POST':
                # POST 요청일 경우 JSON 데이터로 전송
                response = requests.post(url, json=data)  # json은 요청 본문에 JSON 형식으로 데이터를 전달
            else:
                raise ValueError("Unsupported HTTP method")

            # HTTP 상태 코드가 4xx, 5xx인 경우 예외 발생
            response.raise_for_status()
            return response.json().get("data", {})

        except HTTPError as http_err:
            return {'error': f"HTTP error occurred: {http_err}, Response: {response.text}"}
        except RequestException as e:
            return {'error': f"Request error occurred: {e}"}

    def get(self, request, *args, **kwargs):
 
        email_id = request.query_params.get('email_id')
        user_info = self.make_api_request('GET', 'users/', {'email_id': email_id})

        if user_info:
            return response.Response({"success": True, "data": user_info})
        elif email_id:
            return response.Response({"success": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return response.Response({"success": True, "data": []})

    def post(self, request, *args, **kwargs):

        user_data = {
            'username': request.data.get('username'),
            'phone_number': request.data.get('phone_number'),
            'email_id': request.data.get('email_id'),
            'emergency_contact_phone': request.data.get('emergency_contact_phone')
        }

        # 필수 정보가 없으면 에러 응답
        if not all(user_data.values()):
            return response.Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # 선택적 정보 받기 (기타 정보는 request.data로 받을 수 있습니다)
        optional_fields = {key: value for key, value in request.data.items() if key not in user_data}
        user_data.update(optional_fields)

        # 외부 API에 유저 정보 전달
        result = self.make_api_request('POST', 'users/', user_data)

        if 'error' in result:
            return response.Response({'error': result['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response.Response(result, status=status.HTTP_200_OK)
