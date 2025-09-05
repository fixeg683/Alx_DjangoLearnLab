from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms

from .models import Book, Library

# ----------------------------------
# Simple form for Book
# ----------------------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


# ----------------------------------
# Permission-protected book views
# ----------------------------------
@permission_required("relationship_app.can_add_book")
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "relationship_app/book_form.html", {"form": form, "action": "Add"})


@permission_required("relationship_app.can_change_book")
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/book_form.html", {"form": form, "action": "Edit"})


@permission_required("relationship_app.can_delete_book")
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/book_confirm_delete.html", {"book": book})
