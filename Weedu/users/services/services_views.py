import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail

from users.models import Weedu_User

def register_user(user_data):

    token = uuid.uuid4().hex

    cache.set(token, user_data, timeout=180)

    verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}/"

    send_mail(
        subject="Підтвердження Email",
        message=f"Привіт, {user_data['username']}! Для підтвердження вашої електронної пошти перейдіть за посиланням: {verification_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_data['email']],
    )

    return token


def activate_email(token):

    user_data = cache.get(token)

    if user_data:

        user = Weedu_User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )

        cache.delete(token)

        return user

    return None


def login_user(user):

    refresh = RefreshToken.for_user(user)

    try:

        user_data = Weedu_User.objects.get(username=str(user))

    except Weedu_User.DoesNotExist:

        return None

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
        "user": {
            "username": user_data.username,
            "pk": user_data.pk,
            "email": user_data.email
        }
    }


def get_user_data_by_username(username):

    try:

        user = Weedu_User.objects.get(username=username)

        return {
            "username": user.username,
            "email": user.email,
            "experience": user.experience,
            "level": user.level,
            "praise": user.praise,
            "is_active": user.is_active,
            "registered_at": user.registered_at
        }

    except Weedu_User.DoesNotExist:

        raise Response({"errors": {"message": 'User does not exist.'}})
