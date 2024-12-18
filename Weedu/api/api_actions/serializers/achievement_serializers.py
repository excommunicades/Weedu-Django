from rest_framework import serializers

from publish.models.models import Achievement, UserAchievement

class CreateAchievementSerializer(serializers.ModelSerializer):

    """Serializer from json to db data for creation fields"""

    class Meta:

        model = Achievement

        fields = [
            'pk',
            'title',
            'description',
            'image',
            'xp',
            'rarity',
            ]
        extra_kwargs = {'image': {'required': False}}


class GetUserAchievementSerializer(serializers.ModelSerializer):

    """transform from json to db data for creation fields"""

    class Meta:

        model = UserAchievement

        fields = [
            'user',
            'achievement',
            'achieved_at',
            ]

    def create(self, validated_data):

        user = self.context['request'].user
        
        validated_data['user'] = user
        
        return super().create(validated_data)
