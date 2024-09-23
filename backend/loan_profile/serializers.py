"""
Serializers for the loan_profile app.
"""

from rest_framework import serializers
from core.models import LoanProfile


class LoanProfileSerializer(serializers.ModelSerializer):
    """Serializer for loan profile objects."""

    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = LoanProfile
        fields = (
            'id',
            'user',
            'user_name',
            'status',
            'photoURL',
            'business_type',
            'loan_duration_months',
            'total_amount_required',
        )
        read_only_fields = ('id', 'user', 'status', 'user_name')


class LoanProfileDetailSerializer(LoanProfileSerializer):
    """Serializer for loan profile detail objects."""

    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = LoanProfile
        fields = LoanProfileSerializer.Meta.fields + (
            'description',
            'amount_lended_to_date',
            'deadline_to_receive_loan',
            'user_name',
        )
        read_only_fields = ('id', 'user', 'status', 'user_name')
