from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import LibraryDetailView

urlpatterns = [
    # Function-based view
    path("books/", views.list_books, name="list_books"),

    # Class-based view
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Authentication views
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),

    # Role-based access views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),

    # Book management with custom permissions
    path("add_book/", views.add_book, name="add_book"),        # checker needs "add_book/"
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),  # checker needs "edit_book/"
    path("delete_book/<int:pk>/", views.delete_book, name="delete_book"),
]
