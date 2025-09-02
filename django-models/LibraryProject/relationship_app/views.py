from django.shortcuts import render
from .models import Book

# Function-based view (list all books)
def list_books(request):
    books = Book.objects.select_related("author").all()
    return render(request, "relationship_app/list_books.html", {"books": books})
