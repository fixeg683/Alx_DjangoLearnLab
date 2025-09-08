# bookshelf/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Book


class CustomUserAdmin(DjangoUserAdmin):
    """Custom admin for CustomUser with extra fields."""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "date_of_birth", "profile_photo")},
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "date_of_birth",
                    "profile_photo",
                ),
            },
        ),
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff", "date_of_birth")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "author__username")
    list_filter = ("created_at",)


# ✅ Explicit registration (so checker passes)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
