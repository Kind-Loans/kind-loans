"""
Views for the loan_profile app.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import LoanProfile
from loan_profile import serializers


class LoanProfileViewSet(viewsets.ModelViewSet):
    """View for managing loan profiles."""
    serializer_class = serializers.LoanProfileDetailSerializer
    queryset = LoanProfile.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Return objects in reverse order."""
        return self.queryset.order_by('-id')

    def get_permissions(self):
        """Return permissions based on action."""
        if self.action == 'list':
            return []
        return super().get_permissions()

    def get_serializer_class(self):
        """Return the serializer class."""
        if self.action == 'list':
            return serializers.LoanProfileSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new loan profile."""
        serializer.save(user=self.request.user)
