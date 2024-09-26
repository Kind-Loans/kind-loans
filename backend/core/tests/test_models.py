"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from decimal import Decimal


class ModelTests(TestCase):
    """Test user model"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that the email is normalized for new users"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2Example.com", "Test2Example.com"],
        ]
        for email, normalized_email in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, normalized_email)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "sample123")

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@example.com", "testpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_loan_profile(self):
        """Test creating a new loan profile"""
        user = get_user_model().objects.create_user(
            "test@example.com", "testpass123"
        )
        loan_profile = models.LoanProfile.objects.create(
            user=user,
            photoURL="www.example.com/photo.jpg",
            title="Test title",
            description="Test description",
            business_type=1,
            loan_duration_months=12,
            total_amount_required=Decimal("500.00"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )
        self.assertEqual(str(loan_profile), f"{user.name}'s loan profile")


class TransactionModelTests(TestCase):
    def setUp(self):
        password = "testpass123"

        self.user_with_two_loan_profiles = (
            get_user_model().objects.create_user(
                email="test@example.com", password=password
            )
        )

        self.loan_profile_with_transactions = (
            models.LoanProfile.objects.create(
                user=self.user_with_two_loan_profiles,
                photoURL="www.example.com/photo.jpg",
                description="loan profile 1",
                business_type=1,
                loan_duration_months=12,
                total_amount_required=Decimal("500.00"),
                deadline_to_receive_loan="2021-12-31",
                status=1,
            )
        )
        self.loan_profile_without_transactions = (
            models.LoanProfile.objects.create(
                user=self.user_with_two_loan_profiles,
                photoURL="www.example.com/photo.jpg",
                description="loan profile 2",
                business_type=2,
                loan_duration_months=12,
                total_amount_required=Decimal("500.00"),
                deadline_to_receive_loan="2021-12-31",
                status=1,
            )
        )
        self.lender = get_user_model().objects.create_user(
            email="lender@example.com", password=password
        )

    def test_amount_lended_to_date(self):
        """Test amount lended to loan is based on completed transactions"""
        models.Transaction.objects.create(
            loan_profile=self.loan_profile_with_transactions,
            user=self.lender,
            amount=100,
            payment_method=models.PaymentMethod.PAYPAL,
            status=models.TransactionStatus.COMPLETED,
        )
        models.Transaction.objects.create(
            loan_profile=self.loan_profile_with_transactions,
            user=self.lender,
            amount=100,
            payment_method=models.PaymentMethod.PAYPAL,
            status=models.TransactionStatus.COMPLETED,
        )
        models.Transaction.objects.create(
            loan_profile=self.loan_profile_with_transactions,
            user=self.lender,
            amount=100,
            payment_method=models.PaymentMethod.PAYPAL,
            status=models.TransactionStatus.PENDING,
            # pending transactions excluded
        )

        self.assertEqual(
            self.loan_profile_without_transactions.amount_lended_to_date, 0
        )
        self.assertEqual(
            self.loan_profile_with_transactions.amount_lended_to_date, 200
        )
