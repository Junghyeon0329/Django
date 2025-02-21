from rest_framework.throttling import UserRateThrottle
from rest_framework import viewsets, permissions, response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from notices import models, serializers
from custom import * # CustomPagination

class OneSecondThrottle(UserRateThrottle): 
	rate = '1/second'	 

class NoticeViewSet(viewsets.ModelViewSet):
	queryset = models.Notice.objects.all().order_by("-id")
	serializer_class = serializers.NoticeSerializer
	pagination_class = CustomPagination
 
	def get_serializer_class(self):
		return serializers.NoticeSerializer

	def get_throttles(self):
		throttles = super().get_throttles()
		if self.action in ['create', 'partial_update', 'destroy']:
			throttles.append(OneSecondThrottle())			
		return throttles

	def get_permissions(self):
		permission = [] 
		if self.request.method in ['POST', 'PATCH', 'DELETE']:			
			permission.append(permissions.IsAdminUser())			
		return permission

	def get_authenticators(self):
		if self.request.method in ['GET']: 
			return []
		else:	
			return [JWTAuthentication()]

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
			return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
  
