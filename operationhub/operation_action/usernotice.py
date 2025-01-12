from rest_framework import status, response, views, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Notice
from .serializers import NoticeSerializer
from .authentication import OneSecondThrottle
from custom import *

class NoticeAPIView(views.APIView):
	pagination_class = CustomPagination
 
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.request.method == 'POST': 
			throttles.append(OneSecondThrottle())
		elif self.request.method == 'DELETE': 
			throttles.append(OneSecondThrottle())
		return throttles    

	def get_permissions(self):
		permission = []  
		if self.request.method in ['POST', 'DELETE']:			
			permission.append(permissions.IsAdminUser())
	
		return permission

	def get_authenticators(self):
		if self.request.method == 'GET':
			return []

		return [JWTAuthentication()]

	""" GET 요청: 게시글 목록 가져오기 """
	def get(self, request, *args, **kwargs):
				
		queryset = Notice.objects.all().order_by('-created_at')
		
		# Pagination 적용
		paginator = self.pagination_class()  # CustomPagination 인스턴스 생성
		paginated_data = paginator.paginate_queryset(queryset, request)
		
		# 직렬화 (serialize) 처리
		serializer = NoticeSerializer(paginated_data, many=True)

		# 전체 게시글 수를 가져오기
		total_count = queryset.count()

		# 페이지네이션 정보와 함께 직렬화된 데이터를 반환
		return response.Response({
			'total_count': total_count,  # 전체 게시글 수
			'results': serializer.data,   # 직렬화된 게시글 데이터
			'pagination': paginator.get_paginated_response(serializer.data).data  # 페이지네이션 정보
		})

	""" POST 요청: 게시글 생성 """
	def post(self, request, *args, **kwargs):
	   
		serializer = NoticeSerializer(data=request.data, context={'request': request})
		
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
			board = Notice.objects.get(id=board_id)
   
		except Notice.DoesNotExist:
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