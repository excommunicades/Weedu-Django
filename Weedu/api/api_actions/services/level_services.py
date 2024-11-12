from rest_framework import serializers

from rest_framework.response import Response

from users.models import Weedu_User


def user_level_up(request, serializer):

    try:

        user = Weedu_User.objects.get(username=request.user)

        user.expirience += serializer.data.get('expirience')

        if user.expirience >= 100:

            while user.expirience > 100:

                user.level += 1

                user.expirience -= 100

        user.save()

    except Weedu_User.DoesNotExist:

        raise serializers.ValidationError({'error': "User does not exist."})

    return None