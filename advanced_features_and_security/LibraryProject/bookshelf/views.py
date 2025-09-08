# bookshelf/views.py
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages

from .forms import BookForm, SecureSearchForm
from .models import Book


@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    form = SecureSearchForm(request.GET or None)
    qs = Book.objects.select_related("author").order_by("-created_at")

    if form.is_valid():
        term = form.cleaned_term()
        if term:
            # Safe ORM filtering avoids SQL injection
            qs = qs.filter(title__icontains=term)

    return render(request, "bookshelf/book_list.html", {"books": qs, "form": form})


@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user  # using settings.AUTH_USER_MODEL
            book.save()
            messages.success(request, "Book created ✅")
            return redirect(reverse("bookshelf:book_list"))
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form, "title": "Create Book"})


@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated ✏️")
            return redirect(reverse("bookshelf:book_list"))
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form, "title": "Edit Book"})


@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk: int):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted 🗑️")
        return redirect(reverse("bookshelf:book_list"))
    return render(request, "bookshelf/form_example.html", {"form": None, "title": f"Delete {book.title}?"})
