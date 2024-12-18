
from rest_framework import status, views, response
from .serializers import UserProfileSerializer
"""
    start nginx.exe
    nginx -s stop
"""

class UserProfileUploadView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # 모델에 저장
            
            return response.Response(
					{"success": True, "message": "profile picture created successfully."},
					status=status.HTTP_201_CREATED
				)
        
        return response.Response(
				{"success": False, "message": f"{serializer.errors}"},
				status=status.HTTP_400_BAD_REQUEST
			)