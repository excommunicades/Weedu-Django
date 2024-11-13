from rest_framework import generics, status

from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNDIyNzQyLCJpYXQiOjE3MzE0MjI0NDIsImp0aSI6Ijk5NzVhZjU5MTE3NDQwYzI4ZDAxZjFhN2RiYTM5NjM2IiwidXNlcl9pZCI6M30.ZtsRkGMxB6wM_gTx2YpZv_XoXlpw9PgSdiDAwTzpofY

# {
#     "username": "test_name",
#     "email": "test_email@gmail.com",
#     "password": "password1%",
#     "confirm_password": "password1%"
# }

from users.models import Weedu_User
from publish.models.models import Award, UserAward

from api.api_actions.serializers.award_serializers import(
    CreateAwardSerializer,
    GetUserAwardSerializer,
)

# from api.api_actions.services.level_services import (
#     user_level_up
# )


class Awards(generics.GenericAPIView):

    """Endpoint for xp getting"""

    authentication_classes = [SessionAuthentication, JWTAuthentication]

    queryset = Award.objects.all()
    serializer_class = CreateAwardSerializer

    def get(self, request, *args, **kwargs):

        if kwargs.get('pk'):

            try:
                obj = self.get_object()

                serializer = self.get_serializer(obj)

                return Response(serializer.data)

            except Award.DoesNotExist:

                return Response({"error": "Award not found"}, status=status.HTTP_404_NOT_FOUND)
        else:

            data = self.get_queryset()

            serializer = self.get_serializer(data, many=True)

            return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({"message": "successfull"})

        errors = serializer.errors

        formatted_errors = {}

        for field, error in errors.items():
            formatted_errors[field] = error[0]

        print(formatted_errors)

        return Response({"errors": formatted_errors}, status=400)

    def put(self, request, *args, **kwargs):

        obj = self.get_object()

        serializer = self.get_serializer(obj, data=request.data)

        if serializer.is_valid():
            try:

                serializer.save()

                return Response({"message": "Successfully updated"})

            except Exception as e:

                print(f"Error saving object: {e}")

                return Response({"error": "Failed to update object"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        formatted_errors = {field: error[0] for field, error in serializer.errors.items()}

        print(formatted_errors)

        return Response({"errors": formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):

        obj = self.get_object()

        serializer = self.get_serializer(obj, data=request.data)

        user = request.user

        if serializer.is_valid():

            try:

                serializer.save()

                return Response({"message": "Successfully updated"})

            except Exception as e:

                print(f"Error saving object: {e}")

                return Response({"error": "Failed to update object"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        formatted_errors = {field: error[0] for field, error in serializer.errors.items()}

        print(formatted_errors)

        return Response({"errors": formatted_errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, *args, **kwargs):

        user = request.user

        obj = self.get_object()

        obj.delete()

        return Response({"message":" Award successfully deleted."},status=status.HTTP_204_NO_CONTENT)


class Get_User_Award(generics.CreateAPIView):

    """Endpoint for user getting award"""

    queryset = UserAward.objects.all()
    serializer_class = GetUserAwardSerializer
