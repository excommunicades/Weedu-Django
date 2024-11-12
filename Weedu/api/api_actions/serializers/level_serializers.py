from rest_framework import serializers, status

from users.models import Weedu_User

class GetXPSerializer(serializers.Serializer):

    """Serializer for xp getting data"""

    expirience = serializers.IntegerField(required=True)
