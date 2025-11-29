from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# -------------------------------------------------
# Book List View – GET /books/
# Anyone can view the list of books.
# -------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]    # Read-only for everyone


# -------------------------------------------------
# Book Detail View – GET /books/<pk>/
# Anyone can view a single book.
# -------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------------------------
# Book Create View – POST /books/create/
# Only authenticated users can create books.
# -------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Custom behavior (optional)
    def perform_create(self, serializer):
        """
        You can add custom logic here, such as:
        - Automatically associating created books with a user
        - Logging actions
        - Sanitizing data before saving
        """
        serializer.save()


# -------------------------------------------------
# Book Update View – PUT/PATCH /books/<pk>/update/
# Only authenticated users can update books.
# -------------------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update logic goes here.
        """
        serializer.save()


# -------------------------------------------------
# Book Delete View – DELETE /books/<pk>/delete/
# Only authenticated users can delete books.
# -------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
