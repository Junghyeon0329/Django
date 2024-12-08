from django.shortcuts import render

from rest_framework import viewsets, serializers, response
from personal_data.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			"id",
			"name",
			"phone_number",
			"email_id",
            "position",
		]	

# urlpatterns = [
#     path("permissions/", PermissionViewSet.as_view({
#         "get": "list", #모든 객체의 리스트 반환
#         "post": "create" #새 객체를 생성
#     })),
#     path("permissions/<int:pk>/", PermissionViewSet.as_view({
#         "get": "retrieve", #특정 객체를 반환
#         "put": "update", # 특정 객체를 수정
#         "patch": "partial_update", #특정 객체를 일부 수정
#         "delete": "destroy" #특정 객체 삭제
#     })),
# ]

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def list(self, request, *args, **kwargs):
		email_id = request.query_params.get('email_id', None)
		queryset = self.get_queryset()
		if email_id is not None:
			queryset = queryset.filter(email_id=email_id)
			if len(queryset) != 1: 
				queryset = None
			else: 
				serializer = self.get_serializer(queryset.first())
				return response.Response({"success": True, "data": serializer.data})				
		serializer = self.get_serializer(queryset, many=True)
		return response.Response({"success": True, "data": serializer.data})

	def create(self, request, *args, **kwargs):
		email_id = request.query_params.get('email_id', None)
		email_id = request.query_params.get('email_id', None)
		email_id = request.query_params.get('email_id', None)

		username = request.data.get('username')
		email = request.data.get('email')
		password = request.data.get('password')
		is_superuser = request.data.get('is_superuser', False)  # 기본값은 False
		is_staff = request.data.get('is_staff', False)  
		최정현
  
		queryset = self.get_queryset()
		if email_id is not None:
			queryset = queryset.filter(email_id=email_id)
			if len(queryset) != 1: 
				queryset = None
			else: 
				serializer = self.get_serializer(queryset.first())
				return response.Response({"success": True, "data": serializer.data})				
		serializer = self.get_serializer(queryset, many=True)
		return response.Response({"success": True, "data": serializer.data})
	