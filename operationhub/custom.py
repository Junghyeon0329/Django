from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # 한 페이지에 10개씩 데이터 표시
    page_size_query_param = 'page_size'  # 클라이언트가 page_size 파라미터를 전달할 수 있게 설정
    max_page_size = 100  # 최대 페이지 크기 제한