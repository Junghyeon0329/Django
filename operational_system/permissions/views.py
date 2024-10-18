from django.shortcuts import render

from rest_framework import viewsets, serializers
from custom import *
from permissions.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		# fields = ["id", "code", "name", "description"]
		fields = '__all__'

class PermissionViewSet(viewsets.ModelViewSet):
	queryset = Permission.objects.all().order_by("-id")
	serializer_class = PermissionSerializer
	pagination_class = CustomPagination
 


