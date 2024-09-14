"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from cities_light.models import Country, City


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save, and return a new user."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save, and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'
        user.save(using=self._db)

        return user


class UserRole(models.TextChoices):
    """User roles."""
    LENDER = 'lender', 'Lender'
    BORROWER = 'borrower', 'Borrower'
    ADMIN = 'admin', 'Admin'


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""
    email = models.EmailField(
        max_length=255,
        unique=True,
        help_text="The email address of the user."
    )
    name = models.CharField(
        max_length=255,
        help_text="The full name of the user."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site."
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.BORROWER,
        help_text="The role of the user in the system."
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The country where the user is located."
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The city where the user is located."
    )
    business_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="The name of the user's business, if applicable."
    )
    business_category = models.CharField(
        max_length=255,
        blank=True,
        help_text="The category of the user's business, if applicable."
    )
    interests = models.TextField(
        blank=True,
        help_text="The interests of the user."
    )
    photoURL = models.URLField(
        blank=True,
        help_text="The URL of the user's photo."
    )
    story = models.TextField(
        blank=True,
        help_text="The personal story of the user."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the user was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the user was last updated."
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['email']

    def __str__(self):
        return self.email
