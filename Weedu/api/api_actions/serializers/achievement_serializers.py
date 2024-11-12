from rest_framework import serializers

from publish.models.models import Achievement

class CreateAchievementSerializer(serializers.ModelSerializer):

    """Serializer transformed data to json for creation fields"""

    class Meta:

        model = Achievement

        fields = [
            'title',
            'description',
            'image',
            'xp',
            'rarity',
            ]
        extra_kwargs = {'image': {'required': False}}

