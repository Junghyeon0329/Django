from django.shortcuts import render
from rest_framework import viewsets, serializers, response, views, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User

import requests
from requests.exceptions import RequestException, HTTPError

class WorkforceAPIView(views.APIView):

    def get_permissions(self):
        
        permissions = [IsAuthenticated()]
        if self.request.method in ['POST','GET']:
            permissions.append(IsAdminUser())
        return permissions

    """ 새로운 인사 인원 생성 API"""
    def post(self, request, *args, **kwargs):

        user_data = {
            'username': request.data.get('username'),
            'phone_number': request.data.get('phone_number'),
            'email_id': request.data.get('email_id'),
            'emergency_contact_phone': request.data.get('emergency_contact_phone')
        }

        # 필수 정보가 없으면 에러 응답
        if not all(user_data.values()):
            return response.Response(
                {"success": False, "message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 선택적 정보 받기 (기타 정보는 request.data로 받을 수 있습니다)
        optional_fields = {key: value for key, value in request.data.items() if key not in user_data}
        user_data.update(optional_fields)
    
        # 외부 API에 유저 정보 전달 및 결과 처리
        try:
            from URLaddress import workforceURL
            url = f"http://{workforceURL['ip']}:{workforceURL['port']}/users/"

            # POST 요청 전송
            response = requests.post(url, json=user_data)

            # HTTP 상태 코드가 4xx, 5xx인 경우 예외 발생
            response.raise_for_status()

            # 결과 반환
            result = response.json().get("data", {})
            return response.Response(result, status=status.HTTP_200_OK)

        except HTTPError as http_err:
            return response.Response(
                    {"success": False, "message": f"Error: {str(http_err)}."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
          
        except RequestException as e:
            return response.Response(
                    {"success": False, "message": f"Error: {str(e)}."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    """ 인사 인원 정보 요청 API"""
    def get(self, request, *args, **kwargs):
        # 쿼리 파라미터에서 email_id 가져오기
        email_id = request.query_params.get('email_id')

        # URL 설정
        try:
            from URLaddress import workforceURL
            url = f"http://{workforceURL['ip']}:{workforceURL['port']}/users/"

            # GET 요청 전송
            if email_id:
                response = requests.get(url, params={'email_id': email_id})
            else:
                response = requests.get(url)

            # HTTP 상태 코드가 4xx, 5xx인 경우 예외 발생
            response.raise_for_status()

            # 데이터 처리
            user_info = response.json().get("data", {})

            if user_info:
                return response.Response(
                   {"success": True, "message": user_info},
                    status=status.HTTP_200_OK
                )
            else:                
                return response.Response(
                    {"success": False, "message": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except HTTPError as http_err:
            return response.Response(
                    {"success": False, "message": f"Error: {str(http_err)}."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
          
        except RequestException as e:
            return response.Response(
                    {"success": False, "message": f"Error: {str(e)}."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )