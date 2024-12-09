from rest_framework import status, response, views
from .models import Board
from .serializers import BoardSerializer
from rest_framework.permissions import IsAuthenticated

class BoardAPIView(views.APIView):
    
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능
    
    # GET 요청: 게시글 목록 가져오기
    def get(self, request, *args, **kwargs):
        boards = Board.objects.all().order_by('-created_at')
        serializer = BoardSerializer(boards, many=True)  # 여러 개의 게시글을 직렬화
        return response.Response(serializer.data)  # 직렬화된 데이터 반환

    # POST 요청: 게시글 생성
    def post(self, request, *args, **kwargs):
        
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():            
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

