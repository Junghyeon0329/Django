from rest_framework import status, response, views
from .models import Board
from .serializers import BoardSerializer
from rest_framework.permissions import IsAuthenticated

class BoardAPIView(views.APIView):
	
	permissions = [IsAuthenticated]
	
	# GET 요청: 게시글 목록 가져오기
	def get(self, request, *args, **kwargs):
		user_id = request.query_params.get('user_id', None)
		if request.user.is_superuser or request.user.is_staff:	
			if user_id:
				boards = Board.objects.filter(author_id=user_id).order_by('-created_at')
			else:
				boards = Board.objects.all().order_by('-created_at')            
		else:
			# 일반 사용자는 자신의 게시글만 조회할 수 있음
			if user_id:
				# 일반 사용자가 자신 외의 다른 사람의 게시글을 요청하면 403 Forbidden 에러 반환
				if int(user_id) != request.user.id:
					return response.Response({"detail": "You are not authorized to view this user's posts."}, status=status.HTTP_403_FORBIDDEN)
			
			# 일반 사용자는 자신의 게시글만 조회
			boards = Board.objects.filter(author=request.user).order_by('-created_at')
		
		serializer = BoardSerializer(boards, many=True)  # 여러 개의 게시글을 직렬화
		return response.Response(serializer.data)  # 직렬화된 데이터 반환

	# POST 요청: 게시글 생성
	def post(self, request, *args, **kwargs):
		serializer = BoardSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():     
			serializer.save()
			return response.Response(serializer.data, status=status.HTTP_201_CREATED)
		
		return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
