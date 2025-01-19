
from django.contrib.auth import tokens, models
from rest_framework import response, status, views
from django.utils import http, encoding

class PasswordResetConfirmView(views.APIView):
    def put(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')
        new_password = request.data.get('password')
        
        try:
            user_id = encoding.force_str(http.urlsafe_base64_decode(uid))
            user = models.User.objects.get(pk=user_id)

            
            if tokens.default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()

                return response.Response(
                    {"success": True, "message": "Password reset successfully."},
                    status=status.HTTP_200_OK
                )
            else:
                return response.Response(
                    {"success": False, "message": "Invalid token."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except models.User.DoesNotExist:
            return response.Response(
                {"success": False, "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )