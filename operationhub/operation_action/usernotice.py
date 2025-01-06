from rest_framework import status, response, views, permissions
from .models import Notice
from .serializers import NoticeSerializer
from .authentication import OneSecondThrottle
from custom import *

class NoticeAPIView(views.APIView):
	pagination_class = CustomPagination
 
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.request.method == 'POST':  # POST 요청에 대해서만 1초 제한을 적용
			throttles.append(OneSecondThrottle())
		return throttles    

	def get_permissions(self):
		permission = []  
		if self.request.method in ['POST']:			
			permission.append(permissions.IsAdminUser())
		return permission
		
	""" GET 요청: 게시글 목록 가져오기 """
	def get(self, request, *args, **kwargs):
		
		page = request.query_params.get('page', 1)  # 기본 값 1로 설정
				
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