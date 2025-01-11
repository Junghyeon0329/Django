from rest_framework.views import APIView
from rest_framework import response, status, permissions
from django.http import FileResponse
import os
from django.conf import settings

class FileAPIView(APIView):
	
	""" 권한 설정 메서드. """
	def get_permissions(self):
		permission_classes = []    
		if self.request.method in ['GET']:
			permission_classes.append(permissions.IsAuthenticated())
		return permission_classes  

	def get(self, request, *args, **kwargs):
		try:
			file_type = request.GET.get('fileType')
			
			if not file_type:
				return response.Response(
					{"error": "fileType parameter is required"},
					status=status.HTTP_400_BAD_REQUEST
				)
    
			# file_path = os.path.join('files/', f"{file_type}.pdf")
			file_path = os.path.join(settings.MEDIA_ROOT, 'files', "testtest.csv")
			if not os.path.exists(file_path):
				return response.Response(
					{"error": "File not found"},
					status=status.HTTP_404_NOT_FOUND
				)
			return FileResponse(open(file_path, 'rb'), content_type='application/csv')   

		except Exception as e:
			return response.Response(
				{"error": str(e)},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
