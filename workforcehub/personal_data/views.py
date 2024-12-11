from django.shortcuts import render

from rest_framework import viewsets, serializers, response
from personal_data.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "name", "phone_number", "email_id", "position", ]	

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
				return response.Response({"success": True, "data": serializer.data})				
		serializer = self.get_serializer(queryset, many=True)
		return response.Response({"success": True, "data": serializer.data})
