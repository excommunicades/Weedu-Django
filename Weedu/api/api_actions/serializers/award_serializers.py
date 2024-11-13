from rest_framework import serializers

from publish.models.models import Award, UserAward

class CreateAwardSerializer(serializers.ModelSerializer):

    """Serializer from json to db data for creation fields"""

    class Meta:

        model = Award

        fields = [
            'title',
            'description',
            'image',
            'created_at'
            ]

        extra_kwargs = {'image': {'required': False}}


class GetUserAwardSerializer(serializers.ModelSerializer):

    """transform from json to db data for creation fields"""

    class Meta:

        model = UserAward

        fields = [
            'user',
            'award',
            'awarded_at',
            ]

    def create(self, validated_data):

        user = self.context['request'].user
        
        validated_data['user'] = user
        
        return super().create(validated_data)
