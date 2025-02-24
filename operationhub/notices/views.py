
from rest_framework import viewsets, permissions, response, status
from django.db import transaction
from notices import models, serializers
import custom

class NoticeViewSet(viewsets.ModelViewSet):
	queryset = models.Notice.objects.all().order_by("-id")
	serializer_class = serializers.NoticeSerializer
	pagination_class = custom.CustomPagination
 
	# get_authentication(self)에서는 self.action불가
	def get_serializer_class(self):
		return serializers.NoticeSerializer

	def get_permissions(self):		
		permission = [] 
		if self.action in ['create', 'partial_update', 'destroy']:
			permission.append(permissions.IsAdminUser())			
		return permission

	def get_throttles(self):
		throttles = super().get_throttles()
		if self.action in ['create', 'partial_update', 'destroy']:
			throttles.append(custom.OneSecondThrottle())			
		return throttles

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		# **title, content, author
		serializer = self.get_serializer(data=request.data)
	
		if serializer.is_valid():
			self.perform_create(serializer)
			return response.Response({
					"success": True, "message": "created successfully."},
					status=status.HTTP_201_CREATED
				)   
		else:
			return response.Response({
					"success": False, "message": serializer.errors},
					status=status.HTTP_400_BAD_REQUEST
				)
  
	@transaction.atomic
	def partial_update(self, request, *args, **kwargs):
		board_id = request.data.get("board_id")
  
		if not board_id:
			return response.Response({
				"success": False, "message": "Lack of information."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		try:
			notice_instance = models.Notice.objects.get(id=board_id)
   
		except Exception as e:
			return response.Response({
					"success": False, "message": f"{str(e)}."},
					status=status.HTTP_400_BAD_REQUEST
				)
   
		serializer = self.get_serializer(notice_instance, data=request.data, partial=True)
	   
		if serializer.is_valid():
			serializer.save()
			return response.Response({
					"success": True, "message": "Updated successfully."},
					status=status.HTTP_200_OK
				)
		else:
			return response.Response({
					"success": False, "message": serializer.errors},
					status=status.HTTP_400_BAD_REQUEST
				)

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		board_id = request.data.get("board_id")
  
		if not board_id:
			return response.Response({
				"success": False, "message": "Lack of information."},
				status=status.HTTP_400_BAD_REQUEST
			)
   
		models.Notice.objects.filter(id=board_id).delete()
		return response.Response({
				"success": True, "message": "Deleted successfully."},
				status=status.HTTP_200_OK
		)
  
