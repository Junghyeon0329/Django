from django.shortcuts import render

from rest_framework import viewsets, serializers
from rest_framework.response import Response
from users.models import User
from custom import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			"id",
			"name",
			"phone_number",
			"email_id",
		]	

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def list(self, request, *args, **kwargs):
		email_id = request.query_params.get('email_id', None)
		queryset = self.get_queryset()
		if email_id is not None:
			queryset = queryset.filter(email_id=email_id)
			if len(queryset) != 1: 
				queryset = None
			else: 
				serializer = self.get_serializer(queryset.first())
				return Response({"success": True, "data": serializer.data})				
		serializer = self.get_serializer(queryset, many=True)
		return Response({"success": True, "data": serializer.data})
	