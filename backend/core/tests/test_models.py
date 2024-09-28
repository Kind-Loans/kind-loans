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
            email="lender@example.com",
            password=password,
            role=models.UserRole.LENDER,
        )
        self.non_lender = get_user_model().objects.create_user(
            email="nonlender@example.com",
            password=password,
            role=models.UserRole.BORROWER,
        )

    def test_non_lender_cannot_initiate_transaction(self):
        """Test that a user that is not a lender cannot initiate transaction."""
        with self.assertRaises(ValueError):
            models.Transaction.objects.create_transaction(
                lender=self.non_lender,
                borrower=self.loan_profile_with_transactions,
                amount=100,
            )

    def test_amount_lended_to_date_for_loan_profile_without_transactions_is_zero(
        self,
    ):
        """
        Test the amount lended to date for a loan profile without any transactions
        is zero.
        """
        self.assertEqual(
            self.loan_profile_without_transactions.amount_lended_to_date, 0
        )

    def test_amount_lended_to_date_for_loan_profile_with_pending_transactions_is_zero(
        self,
    ):
        """
        Test amount lended to date for loan profile with pending transactions is zero.
        """
        models.Transaction.objects.create_transaction(
            lender=self.lender,
            borrower=self.loan_profile_with_transactions,
            amount=100,
            status=models.TransactionStatus.PENDING,
        )

        self.assertEqual(
            self.loan_profile_with_transactions.amount_lended_to_date, 0
        )

    def test_amount_lended_to_date_for_loan_profile_with_incomplete_transactions_is_zero(
        self,
    ):
        """
        Test amount lended to date for loan profile with incomplete transactions is zero.
        """
        NONTRANSACTION_STATUSES = [
            status
            for status in list(models.TransactionStatus)
            if status != models.TransactionStatus.COMPLETED
        ]
        for status in NONTRANSACTION_STATUSES:
            models.Transaction.objects.create_transaction(
                lender=self.lender,
                borrower=self.loan_profile_with_transactions,
                amount=100,
                status=status,
            )

        self.assertEqual(
            self.loan_profile_with_transactions.amount_lended_to_date, 0
        )

    def test_amount_lended_to_date_for_loan_profile_with_completed_transactions(
        self,
    ):
        """
        Test amount lended to date for loan profile with completed transactions.
        """
        models.Transaction.objects.create_transaction(
            lender=self.lender,
            borrower=self.loan_profile_with_transactions,
            amount=100,
            status=models.TransactionStatus.COMPLETED,
        )
        models.Transaction.objects.create_transaction(
            lender=self.lender,
            borrower=self.loan_profile_with_transactions,
            amount=100,
            status=models.TransactionStatus.COMPLETED,
        )

        self.assertEqual(
            self.loan_profile_with_transactions.amount_lended_to_date, 200
        )
