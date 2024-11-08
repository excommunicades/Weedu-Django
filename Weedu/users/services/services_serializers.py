from rest_framework import serializers

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

from users.models import Weedu_User

def validate_username_unique(username):

    if Weedu_User.objects.filter(username=username).exists():

        raise serializers.ValidationError("User with this name already exists.")

    return username


def validate_email_unique(email):

    if Weedu_User.objects.filter(email=email).exists():

        raise serializers.ValidationError("User with this email already exists.")

    return email


def validate_password_strength(password):

    if len(password) < 8:

        raise serializers.ValidationError("Password must be at least 8 characters long.")

    elif not any(char.isdigit() for char in password):

        raise serializers.ValidationError("Password must contain at least one digit.")

    elif not any(not char.isalnum() for char in password):

        raise serializers.ValidationError("The password must contain at least one special character.")

    return password


def validate_passwords_match(password, confirm_password):

    if password != confirm_password:

        raise serializers.ValidationError({"confirm_password": "Passwords must match."})


def create_user(username, email, password):

    user = Weedu_User(username=username, email=email)

    user.set_password(password)

    user.save()

    return user


def authenticate_user(username, password):

    user = authenticate(username=username, password=password)

    if user is None:
    
        try:
        
            user = Weedu_User.objects.get(username=username)
        
        except Weedu_User.DoesNotExist:
        
            raise serializers.ValidationError({"username": "User with this username does not exist."})
    
        raise serializers.ValidationError({"password": "Wrong password."})

    return user


def send_password_reset_email(user):

    uid = urlsafe_base64_encode(str(user.pk).encode())

    token = default_token_generator.make_token(user)

    reset_url = f'/password_reset_confirm/{uid}/{token}/'

    full_url = f'{settings.FRONTEND_URL}{reset_url}'

    send_mail(
        'Password Reset Request',
        f'Click the link to reset your password: {full_url}',
        'todo@gmail.com',
        [user.email]
    )


def validate_reset_password_token(uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')

        user = Weedu_User.objects.get(pk=uid)

    except (ValueError, TypeError, Weedu_User.DoesNotExist):

        raise ValueError('Invalid user.')

    if not default_token_generator.check_token(user, token):

        raise ValueError("Invalid or expired token.")

    return user


def reset_user_password(user, new_password):

    user.set_password(new_password)

    user.save()
