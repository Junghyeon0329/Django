from rest_framework.throttling import UserRateThrottle
from rest_framework import viewsets
from notices.models import Notice
from notices.serializers import NoticeSerializer

class OneSecondThrottle(UserRateThrottle): rate = '1/second'	 

class NoticeViewSet(viewsets.ModelViewSet):

	queryset = Notice.objects.all().order_by("-id")
	serializer_class = NoticeSerializer
 
	def get_serializer_class(self):
		return NoticeSerializer

	def get_throttles(self):
		throttles = super().get_throttles()
		if self.action == 'create':
			throttles.append(OneSecondThrottle())
		return throttles
