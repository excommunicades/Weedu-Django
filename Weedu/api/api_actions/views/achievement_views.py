from rest_framework import generics, status

from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


from users.models import Weedu_User
from publish.models.models import Achievement, UserAchievement

from api.api_actions.serializers.achievement_serializers import(
    CreateAchievementSerializer,
    GetUserAchievementSerializer
)


class Achievements(generics.GenericAPIView):

    """Endpoint for xp getting"""

    authentication_classes = [SessionAuthentication, JWTAuthentication]

    queryset = Achievement.objects.all()
    serializer_class = CreateAchievementSerializer

    def get(self, request, *args, **kwargs):

        if kwargs.get('pk'):

            try:
                obj = self.get_object()

                serializer = self.get_serializer(obj)

                return Response(serializer.data)

            except Achievement.DoesNotExist:

                return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)
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

        return Response({"message":" Achievement successfully deleted."},status=status.HTTP_204_NO_CONTENT)


class Get_User_Achievement(generics.CreateAPIView):

    """Endpoint for user getting award"""

    queryset = UserAchievement.objects.all()
    serializer_class = GetUserAchievementSerializer
