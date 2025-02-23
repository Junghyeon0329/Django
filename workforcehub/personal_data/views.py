from rest_framework import viewsets, response, status
from django.contrib.auth import models, login
from rest_framework_simplejwt import authentication, tokens, exceptions
from django.conf import settings
import custom

class UserAuthViewSet(viewsets.ModelViewSet):
	queryset = models.User.objects.all()
	permission_classes = [custom.IsAllowedIP]
 
	def get_throttles(self):
		throttles = super().get_throttles()
		if self.action in ['register']:
			throttles.append(custom.OneSecondThrottle())
		return throttles

	def verify_token(self, request, *args, **kwargs):		
		token_key = request.headers.get("Authorization")		
		if not token_key:
			return response.Response({
				   "success": False, "message": "Token required"},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		if token_key.startswith("Bearer "):
			token_key = token_key.split("Bearer ")[1]
  
		authenticator = authentication.JWTAuthentication()
		
		try:
			validated_token = authenticator.get_validated_token(token_key)
			user = authenticator.get_user(validated_token)
			request.user = user
   
		except (exceptions.InvalidToken, exceptions.AuthenticationFailed):
			return response.Response({
				   "success": False, "message": "Invalid or expired token"},
				status=status.HTTP_400_BAD_REQUEST
			)

		return response.Response({
			"success": True, 
			"message":{"user": request.user.username},
			},status=status.HTTP_200_OK)

  
