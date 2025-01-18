from rest_framework import response, status, permissions, views
from django import http, conf
import os

class FileAPIView(views.APIView):
	
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
					{"success": False, "message": "fileType parameter is required"},
					status=status.HTTP_400_BAD_REQUEST
				)
	
			file_path = os.path.join(conf.settings.MEDIA_ROOT, 'files', f"{file_type}.docx")
			if not os.path.exists(file_path):
				return response.Response(
					{"success": False, "message": "File not found"},
					status=status.HTTP_400_BAD_REQUEST
				)
			return http.FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

		except Exception as e:
			return response.Response(
					{"success": False, "message": str(e)},
					status=status.HTTP_400_BAD_REQUEST
			)
