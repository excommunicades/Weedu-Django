from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import base64

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from users.models import Weedu_User
from users.services.services_serializers import(
    send_password_reset_email,
    validate_reset_password_token,
    reset_user_password,
    authenticate_user,
    create_user,
    validate_passwords_match,
    validate_password_strength,
    validate_email_unique,
    validate_username_unique
    
)

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    """Serializer for user's registration"""

    class Meta:

        """Initialization fields and models"""

        model = Weedu_User

        fields = [
                'username',
                'email',
                'password',
                'confirm_password',
                ]

    def validate_username(self, value):

        """chekcs username on unique in db"""

        return validate_username_unique(value)

    def validate_email(self, value):

        """checks email on unique in db"""

        return validate_email_unique(value)

    def validate_password(self, value):

        """Validates the password strength"""

        return validate_password_strength(value)

    def validate(self, attrs):

        validate_passwords_match(attrs['password'], attrs['confirm_password'])

        return attrs

    def create(self, validated_data):

        validated_data.pop('confirm_password')

        return create_user(validated_data['username'], validated_data['email'], validated_data['password'])


class ActivateEmailSerializer(serializers.Serializer):

    token = serializers.CharField()


class AuthorizationSerializer(serializers.Serializer):

    """Serializer for user's login request"""

    username = serializers.CharField()
    password = serializers.CharField()
    is_cookie = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        if username is None or password is None:
            raise serializers.ValidationError({
                                        "errors": {
                                            "username": "This field is required.",
                                            "password": "This field is required."
                                            }
                                        })

        user = authenticate_user(username, password)

        attrs['user'] = user

        return attrs


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        try:

            user = Weedu_User.objects.get(email=value)

        except Weedu_User.DoesNotExist:

            raise serializers.ValidationError("User with this email does not exist.")

        else:

            return value


    def save(self):

        email = self.validated_data['email']

        user = get_user_model().objects.get(email=email)

        send_password_reset_email(user)


class ResetPasswordConfirmSerializer(serializers.Serializer):

    uibd64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):

        return validate_password_strength(value)

    def validate(self, data):

        validate_reset_password_token(data['uibd64'], data['token'])

        return data

    def save(self):

        uid = urlsafe_base64_decode(self.validated_data['uibd64']).decode('utf-8')

        user = get_user_model().objects.get(pk=uid)

        reset_user_password(user, self.validated_data['new_password'])


class GetUserDataSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.CharField()
    experience = serializers.IntegerField()
    level = serializers.IntegerField()
    praise = serializers.CharField()
    is_active = serializers.BooleanField()
    registered_at = serializers.CharField()
