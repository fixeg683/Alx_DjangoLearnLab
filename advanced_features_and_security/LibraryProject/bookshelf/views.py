# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from .models import Book
from .forms import ExampleForm, BookForm  # ✅ Import ExampleForm


def example_form_view(request):
    """Demo view to handle ExampleForm with CSRF protection."""
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Normally you'd save or process form data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            return render(
                request,
                "bookshelf/form_example.html",
                {"form": form, "success": True, "name": name, "email": email, "message": message},
            )
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """List all books (requires can_view permission)."""
    books = Book.objects.select_related("author").all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    """Create a new book (requires can_create permission)."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    """Edit an existing book (requires can_edit permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form, "book": book})


@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
    """Delete a book (requires can_delete permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})
