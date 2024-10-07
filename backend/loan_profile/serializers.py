"""
Serializers for the loan_profile app.
"""

from rest_framework import serializers
from core.models import LoanProfile, LoanUpdate


class LoanUpdateSerializer(serializers.ModelSerializer):
    loan_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LoanUpdate
        fields = [
            "id",
            "loan_profile",
            "update_type",
            "update_details",
            "timestamp",
        ]


class LoanProfileSerializer(serializers.ModelSerializer):
    """Serializer for loan profile objects."""

    user_name = serializers.CharField(source="user.name", read_only=True)

    updates = LoanUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = LoanProfile
        fields = (
            "id",
            "user",
            "user_name",
            "title",
            "status",
            "photoURL",
            "business_type",
            "loan_duration_months",
            "total_amount_required",
            "amount_lended_to_date",
            "updates",
        )
        read_only_fields = (
            "id",
            "user",
            "status",
            "user_name",
            "amount_lended_to_date",
        )


class LoanProfileDetailSerializer(LoanProfileSerializer):
    """Serializer for loan profile detail objects."""

    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = LoanProfile
        fields = LoanProfileSerializer.Meta.fields + (
            "description",
            "amount_lended_to_date",
            "deadline_to_receive_loan",
            "user_name",
        )
        read_only_fields = ("id", "user", "status", "user_name")
