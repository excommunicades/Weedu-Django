import uuid
from datetime import timedelta

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from django.core.cache import cache
from django.contrib.auth import login

# authentication_classes = [SessionAuthentication, JWTAuthentication]

from users.serializers import (
    RegistrationSerializer,
    ActivateEmailSerializer,
    AuthorizationSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
    GetUserDataSerializer,
    )

from users.services.services_views import (
    register_user,
    activate_email,
    login_user,
    get_user_data_by_username
)

from users.models import Weedu_User





class Register_User(generics.CreateAPIView):

    """Endpoint for user registration"""

    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):

        """Check validation of form, create user"""
        
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            user_data = serializer.validated_data

            token = register_user(user_data)

            cache.set(token, user_data, timeout=180)

            request.session['user_data'] = user_data
            request.session['verification_token'] = token

            return Response(
                {"message": "Registration successful. Please check your email for confirmation."},
                status=status.HTTP_200_OK
            )

        errors = serializer.errors

        formatted_errors = {}


        for error in errors.values():

            e = [k for k, v in errors.items() if v == error]

            formatted_errors[str(e[0])] = str(error[0])

        if errors.get("username"):

            if errors["username"][0] == 'weedu_ user with this username already exists.':

                formatted_errors["username"] = 'User with this name already exists.'

        if errors.get("email"):

            if errors["email"][0] == 'weedu_ user with this email already exists.':

                formatted_errors["email"] = 'User with this email already exists.'



        print(formatted_errors)

        return Response(
            {"errors": formatted_errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class Activate_email(generics.GenericAPIView):

    serializer_class = ActivateEmailSerializer

    def post(self, request, token, *args, **kwargs):

        user = activate_email(token)

        if user:

            return Response({"message": "The e-mail was successfully verified and the user was registered!"}, status=status.HTTP_201_CREATED)

        else:

            return Response({"errors": {"message": "The session is missing user data"}}, status=status.HTTP_400_BAD_REQUEST)


class Login_User(generics.GenericAPIView):

    """Endpoint for user authentication"""

    serializer_class = AuthorizationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():

            errors = serializer.errors

            formatted_errors = {}

            for error in errors.values():

                e = [k for k, v in errors.items() if v == error]

                formatted_errors[str(e[0])] = str(error[0])

            if errors.get("username"):

                if errors["username"][0] == 'weedu_ user with this username already exists.':

                    formatted_errors["username"] = 'User with this username does not exist.'

            if errors.get("email"):

                if errors["email"][0] == 'weedu_ user with this email already exists.':

                    formatted_errors["email"] = 'User with this username does not exist.'

            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        is_cookie = serializer.validated_data.get('is_cookie', False)

        if is_cookie:

            request.session.set_expiry(timedelta(weeks=2))

        else:

            request.session.set_expiry(0)

        login_response = login_user(user)

        if login_response:

            login(request, user)

            request.session['user_data'] = {
                'username': user.username,
                'email': user.email,
                'pk': user.pk
            }

            return Response(login_response, status=status.HTTP_200_OK)

        else:

            return Response({'errors': {'username': 'User not found.'}}, status=status.HTTP_404_NOT_FOUND)

class Reset_password(generics.GenericAPIView):

    """Endpoint for letter submitting"""

    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = ResetPasswordSerializer(data=request.data)

        # Проверяем валидность данных
        if not serializer.is_valid():

            errors = serializer.errors

            formatted_errors = {}

            for error in errors.values():

                e = [k for k, v in errors.items() if v == error]

                formatted_errors[str(e[0])] = str(error[0])

            return Response({'errors': formatted_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'message': 'A link to change your password has been sent to your email address.'}, status=status.HTTP_200_OK)


class Reset_confirm_password(generics.GenericAPIView):

    """Endpoint for confirming password"""

    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request, *args, **kwargs):

        serializer = ResetPasswordConfirmSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():

            serializer.save()

            return Response({"message": "The password was changed successfully"}, status=status.HTTP_205_RESET_CONTENT)

        else:

            if serializer.errors.get('server')[0] == 'Invalid or expired token.':

                return Response({"errors": {"new_password": 'Invalid or expired token.'}},status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Get_user_data(generics.GenericAPIView):

    """Endpoint for getting user data"""

    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = GetUserDataSerializer

    def post(self, request, *args, **kwargs):

        request_user = request.user

        try:

            user_data = get_user_data_by_username(str(request_user))

        except Weedu_User.DoesNotExist as e:

            return Response({"errors": {"message": str(e)}}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_data, status=status.HTTP_200_OK)
