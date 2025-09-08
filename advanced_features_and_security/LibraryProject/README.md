# Advanced Features and Security

## Custom User Model
- Located at `bookshelf.models.User` (extends `AbstractUser`).
- Extra fields: `date_of_birth`, `profile_photo`.
- Manager `UserManager` implements `create_user` and `create_superuser`.
- Set `AUTH_USER_MODEL = "bookshelf.User"` in `LibraryProject/settings.py`.
- Django admin customized in `bookshelf.admin.UserAdmin`.

## Permissions & Groups
- Model `Book` has custom permissions: `can_view`, `can_create`, `can_edit`, `can_delete`.
- Views protected with `@permission_required('bookshelf.can_*', raise_exception=True)`.
- Create groups & assign permissions via:
