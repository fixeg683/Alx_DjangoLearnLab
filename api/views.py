from django.http import JsonResponse
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer


# Root home view (for http://127.0.0.1:8000/)
def home(request):
    return JsonResponse({"message": "Welcome to the API project!"})


# List all books (GET /api/books/)
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Full CRUD for books (GET, POST, PUT, DELETE at /api/books_all/)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
