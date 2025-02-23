from rest_framework import pagination, response, throttling, permissions

ALLOWED_API_KEYS = ['127.0.0.1', 'localhost']
class IsAllowedIP(permissions.BasePermission):    
    def has_permission(self, request, view):
        host = request.get_host().split(":")[0]
        return host in ALLOWED_API_KEYS

class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return response.Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
        
class OneSecondThrottle(throttling.UserRateThrottle): 
	rate = '1/second'

