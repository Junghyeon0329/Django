
from rest_framework import viewsets, permissions, response, status, exceptions, views
from rest_framework_simplejwt import authentication
from django.db import transaction
from notices import models, serializers
import workforce_API
import custom

class NoticeViewSet(viewsets.ModelViewSet):
	queryset = models.Notice.objects.all().order_by("-id")
	serializer_class = serializers.NoticeSerializer
	pagination_class = custom.CustomPagination
 
	def get_serializer_class(self):
		return serializers.NoticeSerializer

	def get_throttles(self):
		throttles = super().get_throttles()
		if self.action in ['create', 'partial_update', 'destroy']:
			throttles.append(custom.OneSecondThrottle())			
		return throttles

	def get_permissions(self):
		print("\nget_permissions\n")
		permission = [] 
		if self.request.method in ['POST', 'PATCH', 'DELETE']:			
			permission.append(permissions.IsAdminUser())			
		return permission
		
  
	def get_authenticators(self):
		if self.request.method in ['GET']: 
			return []
		else:	
			auth = workforce_API.JWTAuthentication()
			res = auth.verify_token(self.request)	
			
			if res.status_code != 200:
				print("\n 토큰이 만료되었습니다. \n")
				return [authentication.JWTAuthentication()]
			return []

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		# **title, content, author
		serializer = self.get_serializer(data=request.data)
	
		if serializer.is_valid():
			self.perform_create(serializer)
			return response.Response(
				{"detail": f"Notice has been successfully created."},
				status=status.HTTP_201_CREATED
			)
		else:
			return response.Response(
				serializer.errors, 
				status=status.HTTP_400_BAD_REQUEST
			)
  
	@transaction.atomic
	def partial_update(self, request, *args, **kwargs):
		
		# **board_id
		board_id = request.data.get("board_id")
  
		if not board_id:
			return response.Response(
				{"detail": "The 'board_id' field is required to delete a notice."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		try:
			notice_instance = models.Notice.objects.get(id=board_id)
		except models.Notice.DoesNotExist:
			return response.Response(
				{"detail": f"Notice is not found."},
				status=status.HTTP_404_NOT_FOUND
			)
   
		serializer = self.get_serializer(notice_instance, data=request.data, partial=True)
	   
		if serializer.is_valid():
			serializer.save()
			return response.Response(
				{"detail": "Notice has been successfully updated."},
				status=status.HTTP_200_OK
			)
		else:
			return response.Response(
				serializer.errors, 
				status=status.HTTP_400_BAD_REQUEST
			)

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		
		# **board_id
		board_id = request.data.get("board_id")
  
		if not board_id:
			return response.Response(
				{"detail": "The 'board_id' field is required to delete a notice."},
				status=status.HTTP_400_BAD_REQUEST
			)
		models.Notice.objects.filter(id=board_id).delete()
		return response.Response(
			{"detail": f"Notice has been successfully deleted."},
			status=status.HTTP_200_OK
		)
  
