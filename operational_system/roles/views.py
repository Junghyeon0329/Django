from django.shortcuts import render

from rest_framework import viewsets, serializers
from custom import *
from roles.models import Role

class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = '__all__'

class RoleViewSet(viewsets.ModelViewSet):
	queryset = Role.objects.all().order_by("-id")
	serializer_class = RoleSerializer
	pagination_class = CustomPagination
