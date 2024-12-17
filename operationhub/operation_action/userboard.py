from rest_framework import status, response, views, permissions
from .models import Board
from .serializers import BoardSerializer
from django.contrib.auth.models import User
from .authentication import OneSecondThrottle

class BoardAPIView(views.APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.request.method == 'POST':  # POST 요청에 대해서만 1초 제한을 적용
			throttles.append(OneSecondThrottle())
		return throttles    
	
	""" POST 요청: 게시글 생성 """
	def post(self, request, *args, **kwargs):
	   
		serializer = BoardSerializer(data=request.data, context={'request': request})
		
		if serializer.is_valid():
			serializer.save()
			return response.Response(
					{"success": True, "message": "Board created successfully."},
					status=status.HTTP_201_CREATED
				)
			
		return response.Response(
				{"success": False, "message": "Board is not valid"},
				status=status.HTTP_400_BAD_REQUEST
			)
	
	""" DELETE 요청: 게시글 삭제 """ 
	def delete(self, request, *args, **kwargs):
	   
		board_id = request.data.get('board_id', None)

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
		
		email = request.query_params.get('email', None)
		if request.user.is_staff:
			if email:
				try:
					# 이메일로 사용자 조회
					user = User.objects.get(email=email)
					# 해당 사용자가 작성한 게시글만 필터링
					boards = Board.objects.filter(author=user)
					
				except User.DoesNotExist:
					return response.Response(
						{"success": False, "message": "User with this email does not exist."},
						status=status.HTTP_404_NOT_FOUND
					)
			else:
				boards = Board.objects.filter(author_id=request.user.id)
		else:    
			# 일반 사용자는 본인만 조회
			if email and email != str(request.user.email):
				return response.Response(
					{"success": False, "message": "You are not authorized to view this user's posts."},
					status=status.HTTP_403_FORBIDDEN
				)
			boards = Board.objects.filter(author_id=request.user.id)

		# 게시글이 없으면 오류 응답 반환
		if not boards.exists():
			return response.Response(
				{"success": False, "message": "No posts found."},
				status=status.HTTP_404_NOT_FOUND
			)

		# 게시글을 직렬화하고 반환
		serializer = BoardSerializer(boards, many=True)
		return response.Response(
			{"success": True, "data": serializer.data},  # 응답 구조화
			status=status.HTTP_200_OK
		)