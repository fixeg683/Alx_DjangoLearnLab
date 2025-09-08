# bookshelf/management/commands/create_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = "Create default groups (Viewers, Editors, Admins) and assign model permissions."

    def handle(self, *args, **options):
        Book = apps.get_model("bookshelf", "Book")

        # Ensure permissions exist
        perms = Permission.objects.filter(content_type__app_label="bookshelf", content_type__model="book")
        perm_map = {p.codename: p for p in perms}

        required = ["can_view", "can_create", "can_edit", "can_delete"]
        missing = [codename for codename in required if codename not in perm_map]
        if missing:
            self.stdout.write(self.style.WARNING(f"Missing permissions (will appear after migrate): {missing}"))

        viewers, _ = Group.objects.get_or_create(name="Viewers")
        editors, _ = Group.objects.get_or_create(name="Editors")
        admins, _ = Group.objects.get_or_create(name="Admins")

        if "can_view" in perm_map:
            viewers.permissions.set([perm_map["can_view"]])
        if all(pm in perm_map for pm in ("can_view", "can_create", "can_edit")):
            editors.permissions.set([perm_map["can_view"], perm_map["can_create"], perm_map["can_edit"]])
        if all(pm in perm_map for pm in ("can_view", "can_create", "can_edit", "can_delete")):
            admins.permissions.set([perm_map["can_view"], perm_map["can_create"], perm_map["can_edit"], perm_map["can_delete"]])

        self.stdout.write(self.style.SUCCESS("Groups and permissions configured."))
