from rest_framework.views import APIView
from rest_framework import response, status, permissions

class FileAPIView(APIView): 
	
	""" 권한 설정 메서드. """
	def get_permissions(self):
		permission_classes = []    
		if self.request.method in ['GET']:
			permission_classes.append(permissions.IsAuthenticated)
		return permission_classes    
	
	def get(self, request, *args, **kwargs):
		return response.Response(
			{"success": True, "message": "Password reset successfully."},
			status=status.HTTP_200_OK
		)
		   