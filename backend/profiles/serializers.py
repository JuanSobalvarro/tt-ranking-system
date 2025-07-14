from rest_framework import serializers
from profiles.models import UserProfile, PlayerProfile, RefereeProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    """
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined',
                  'birth_date', 'sex', 'nationality', 'is_player', 'is_referee', 'image', 'description']
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        """
        Create a new UserProfile instance.
        """
        user = self.context['request'].user
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        """
        Update an existing UserProfile instance.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PlayerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for PlayerProfile model.
    """
    profile = UserProfileSerializer()

    class Meta:
        model = PlayerProfile
        fields = ['id', 'profile', 'alias', 'is_premium', 'handedness', 'play_style', 'grip_type', 'dominance', 'last_operation']
        read_only_fields = ['id', 'last_operation']


class RefereeProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for RefereeProfile model.
    """
    profile = UserProfileSerializer()

    class Meta:
        model = RefereeProfile
        fields = ['id', 'profile', 'alias', 'identifier', 'matches_refereed', 'last_operation']
        read_only_fields = ['id', 'last_operation']

