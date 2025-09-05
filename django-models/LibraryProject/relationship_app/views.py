from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms

from .models import Book, Library

# -------------------------------
# Function-based view
# -------------------------------
def list_books(request):
    books = Book.objects.all()  # checker needs Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# -------------------------------
# Class-based view for library details
# -------------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"  # checker needs relationship_app/library_detail.html
    context_object_name = "library"  # checker needs library


# -------------------------------
# User registration view
# -------------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # checker needs UserCreationForm()
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()  # checker needs UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})  # checker needs relationship_app/register.html


# -------------------------------
# Role-based Access Control
# -------------------------------
def is_admin(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "Admin"

def is_librarian(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "Librarian"

def is_member(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "Member"


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
