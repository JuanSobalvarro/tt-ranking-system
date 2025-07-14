from rest_framework import viewsets, permissions
from profiles.models import UserProfile, PlayerProfile, RefereeProfile
from profiles.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile model.
    Provides list, retrieve, create, update, and destroy actions.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Override to set the user from the request.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Override to update the user profile.
        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """
        Override to handle soft deletion.
        """
        instance.delete()


class PlayerProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PlayerProfile model.
    Provides list, retrieve, create, update, and destroy actions.
    """
    queryset = PlayerProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Override to set the user from the request.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Override to update the player profile.
        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """
        Override to handle soft deletion.
        """
        instance.delete()


class RefereeProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RefereeProfile model.
    Provides list, retrieve, create, update, and destroy actions.
    """
    queryset = RefereeProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Override to set the user from the request.
        """
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """
        Override to update the referee profile.
        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """
        Override to handle soft deletion.
        """
        instance.delete()
