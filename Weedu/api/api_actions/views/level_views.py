from rest_framework import generics, status

from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNDIyNzQyLCJpYXQiOjE3MzE0MjI0NDIsImp0aSI6Ijk5NzVhZjU5MTE3NDQwYzI4ZDAxZjFhN2RiYTM5NjM2IiwidXNlcl9pZCI6M30.ZtsRkGMxB6wM_gTx2YpZv_XoXlpw9PgSdiDAwTzpofY

# {
#     "username": "test_name",
#     "email": "test_email@gmail.com",
#     "password": "password1%",
#     "confirm_password": "password1%"
# }
from users.models import Weedu_User

from api.api_actions.serializers.level_serializers import(
    GetXPSerializer
)

from api.api_actions.services.level_services import (
    user_level_up
)

class GetXp(generics.GenericAPIView):

    """Endpoint for xp getting"""

    authentication_classes = [SessionAuthentication, JWTAuthentication]

    serializer_class = GetXPSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            user = request.user

            if user:

                user_level_up(request=request, serializer=serializer)

                return Response({"message": f"{user} was receveid {serializer.data.get('expirience')} xp"})

            return Response({"error": "User does not exist."})

        errors = serializer.errors

        formatted_errors = {}

        for error in errors.values():

            e = [k for k, v in errors.items() if v == error]

            formatted_errors[str(e[0])] = str(error[0])

        return Response({"errors": formatted_errors}, status=status.HTTP_400_BAD_REQUEST)
