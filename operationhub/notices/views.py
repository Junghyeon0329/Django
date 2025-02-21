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
		if self.action in ['create', 'destroy']:
			throttles.append(OneSecondThrottle())			
		return throttles

	def get_permissions(self):
		permission = [] 
		if self.request.method in ['POST', 'DELETE']:			
			permission.append(permissions.IsAdminUser())			
		return permission

	def get_authenticators(self):
		if self.request.method in ['GET']: 
			return []
		else:	
			return [JWTAuthentication()]

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data) # title, content, author
	
		if serializer.is_valid():
			self.perform_create(serializer)
			return response.Response(serializer.data, status=status.HTTP_201_CREATED)
		return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)