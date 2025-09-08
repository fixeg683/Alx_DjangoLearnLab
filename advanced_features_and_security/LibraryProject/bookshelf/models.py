# bookshelf/models.py
from __future__ import annotations

import os
from datetime import date
from typing import Any

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def profile_photo_upload_to(instance: "CustomUser", filename: str) -> str:
    """Store profile photos inside media/profile_photos/user_<id>/filename"""
    return os.path.join("profile_photos", f"user_{instance.pk or 'new'}", filename)


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser with create_user and create_superuser."""

    use_in_migrations = True

    def _create_user(self, username: str, email: str | None, password: str | None, **extra_fields: Any) -> "CustomUser":
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Validate custom fields
        dob = extra_fields.get("date_of_birth")
        if dob and not isinstance(dob, date):
            raise ValueError("date_of_birth must be a datetime.date instance")

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model extending Django's AbstractUser."""

    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to=profile_photo_upload_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "gif"])],
        help_text=_("Optional profile photo (JPG/PNG/GIF)."),
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.get_username()


class Book(models.Model):
    """Example model with custom permissions."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"),
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
        ]

    def __str__(self) -> str:
        return self.title
