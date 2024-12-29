from rest_framework import status, response, views, permissions
from .models import Notice
from .serializers import NoticeSerializer
from .authentication import OneSecondThrottle
from custom import *

class NoticeAPIView(views.APIView):
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = CustomPagination
 
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.request.method == 'POST':  # POST 요청에 대해서만 1초 제한을 적용
			throttles.append(OneSecondThrottle())
		return throttles    
	
	""" GET 요청: 게시글 목록 가져오기 """
	def get(self, request, *args, **kwargs):
		page = request.query_params.get('page', 1)  # 기본 값 1로 설정
		
		# 게시글 쿼리셋 가져오기 (필터링이나 정렬을 추가할 수 있음)
		queryset = Notice.objects.all()  # 여기서는 모든 게시글을 가져옴
		
		# Pagination 적용
		paginator = self.pagination_class()  # CustomPagination 인스턴스 생성
		paginated_data = paginator.paginate_queryset(queryset, request)
		
		# 직렬화 (serialize) 처리
		serializer = NoticeSerializer(paginated_data, many=True)
		
		# 페이지네이션 정보와 함께 직렬화된 데이터를 반환
		return paginator.get_paginated_response(serializer.data)


  