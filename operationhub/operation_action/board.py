from rest_framework import status, response, views
from .models import Board
from .serializers import BoardSerializer
from rest_framework.permissions import IsAuthenticated

class BoardAPIView(views.APIView):
    permission_classes = [IsAuthenticated]  # permissions 속성은 'permission_classes'로 변경

    def get_error_response(self, message, status_code):
        """
        	공통적인 에러 응답을 생성하는 메서드.
        """
        return response.Response({"detail": message}, status=status_code)

    def get_boards(self, user, user_id=None):
        """
        	사용자에 맞는 게시글을 필터링하여 반환하는 메서드.
        """
        if user.is_superuser or user.is_staff:
            if user_id:
                return Board.objects.filter(author_id=user_id).order_by('-created_at')
            return Board.objects.all().order_by('-created_at')
        
        # 일반 사용자는 자신의 게시글만 조회
        if user_id and int(user_id) != user.id:
            return None  # 다른 사람의 게시글을 요청한 경우 None을 반환하여 403 오류 처리
        
        return Board.objects.filter(author=user).order_by('-created_at')

    def has_delete_permission(self, user, board):
        """
        	게시글 삭제 권한을 확인하는 메서드.
        """
        if user.is_superuser or user.is_staff:
            return True
        return board.author == user 

    def get(self, request, *args, **kwargs):
        """
        	GET 요청: 게시글 목록 가져오기
        """
        user_id = request.query_params.get('user_id', None)
        boards = self.get_boards(request.user, user_id)

        if boards is None:
            return self.get_error_response("You are not authorized to view this user's posts.", status.HTTP_403_FORBIDDEN)

        serializer = BoardSerializer(boards, many=True)
        return response.Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        	POST 요청: 게시글 생성
        """
        serializer = BoardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        	DELETE 요청: 게시글 삭제
        """
        board_id = request.query_params.get('board_id')

        if not board_id:
            return self.get_error_response("Board ID is required.", status.HTTP_400_BAD_REQUEST)
        
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return self.get_error_response("Post not found.", status.HTTP_404_NOT_FOUND)

        if self.has_delete_permission(request.user, board):
            board.delete()
            return response.Response({"success": True, "message": "Board deleted successfully"}, status=status.HTTP_200_OK)

        return self.get_error_response("You are not authorized to delete this post.", status.HTTP_403_FORBIDDEN)
