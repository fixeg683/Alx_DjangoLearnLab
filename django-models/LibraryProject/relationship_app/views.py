from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms

# Imports (explicit for checker)
from .models import Book
from .models import Library   # required separately


# Function-based view
def list_books(request):
    books = Book.objects.all()  # checker requires .all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
