
from rest_framework import status, views, response
from .serializers import UserProfileSerializer

class UserProfileUploadView(views.APIView):
    def post(self, request, *args, **kwargs):
        # 프로필 사진이 포함되어 있는지 확인
        if 'profile_picture' not in request.FILES:
            return response.Response(
                {"success": False, "message": "No profile picture provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # 유저 프로필과 함께 사진을 저장

            return response.Response(
                {"success": True, "message": "Profile picture created successfully."},
                status=status.HTTP_201_CREATED
            )
        
        return response.Response(
            {"success": False, "message": f"{serializer.errors}"},
            status=status.HTTP_400_BAD_REQUEST
        )