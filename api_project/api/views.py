from rest_framework import generics, viewsets
# *** FIX: We must import permissions from rest_framework ***
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from .models import Book
from .serializers import BookSerializer

# This ViewSet provides the implementations for all CRUD operations:
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet that provides full CRUD for the Book model.
    - Permissions: Allows anyone to READ (GET) books, but requires 
      an authenticated user (with a token) to CREATE, UPDATE, or DELETE books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Keeping the old view as requested in the URL pattern instructions
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Apply the same permission for consistency
    permission_classes = [IsAuthenticatedOrReadOnly]