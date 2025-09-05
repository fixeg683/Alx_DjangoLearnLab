from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView
import relationship_app.views as views  # for register + role-based views

urlpatterns = [
    # Function-based and class-based views
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Authentication routes
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),

    # Role-based access control
    path("admin-only/", views.admin_view, name="admin_view"),
    path("librarian-only/", views.librarian_view, name="librarian_view"),
    path("member-only/", views.member_view, name="member_view"),
]
d
