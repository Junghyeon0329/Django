
from rest_framework.pagination import PageNumberPagination

# 127.0.0.1:8000/users/?page=1&page_size=2  
class CustomPagination(PageNumberPagination):
	page_size = 'page'
	page_size_query_param = 'page_size'