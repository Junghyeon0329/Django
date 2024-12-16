from rest_framework import status, response, views, permissions
from .models import Board
from .serializers import BoardSerializer

class BoardAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
     
    """ POST 요청: 게시글 생성 """
    def post(self, request, *args, **kwargs):
       
        serializer = BoardSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """ DELETE 요청: 게시글 삭제 """ 
    def delete(self, request, *args, **kwargs):
       
        board_id = request.query_params.get('board_id')

        # board_id가 없으면 400 오류 반환
        if not board_id:
            return response.Response(
                {"success": False, "message": "Board ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # 게시글을 가져옵니다.
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            # 게시글이 없으면 404 오류 반환
            return response.Response(
                {"success": False, "message": "Post not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 게시글 삭제 권한 확인
        if request.user.is_superuser or request.user.is_staff or board.author == request.user:
            board.delete()  # 권한이 있으면 게시글 삭제
            return response.Response(
                {"success": True, "message": "Board deleted successfully"},
                status=status.HTTP_200_OK
            )
        
        # 권한이 없으면 403 오류 반환
        return response.Response(
            {"success": False, "message": "You are not authorized to delete this post."},
            status=status.HTTP_403_FORBIDDEN
        )
        
    """ GET 요청: 게시글 목록 가져오기 """
    def get(self, request, *args, **kwargs):
        
        user_id = request.query_params.get('user_id', None)
        
        # 관리자일 경우, 모든 게시글을 가져올 수 있음
        if request.user.is_staff:
            boards = Board.objects.filter(user_id=user_id) if user_id else Board.objects.all()
        else:
            # 일반 사용자는 본인 게시글만 볼 수 있음
            boards = Board.objects.filter(user=request.user)
            if user_id and user_id != str(request.user.id):
                return response.Response(
                    {"success": False, "message": "You are not authorized to view this user's posts."},
                    status=status.HTTP_403_FORBIDDEN
                )

        # 게시글이 없으면 오류 응답 반환
        if not boards.exists():
            return response.Response(
                {"success": False, "message": "No posts found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 게시글을 직렬화하고 반환
        serializer = BoardSerializer(boards, many=True)
        return response.Response(serializer.data)
   