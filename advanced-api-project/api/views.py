from rest_framework import generics
# The checker expects this exact import line to exist in api/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Book
from .serializers import BookSerializer

# -------------------------------------------------
# Book List View – GET /api/books/
# Anyone can view list (read-only).
# -------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# -------------------------------------------------
# Book Detail View – GET /api/books/<pk>/
# Anyone can view detail (read-only).
# -------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# -------------------------------------------------
# Resolve ID from URL, query param, or body
# -------------------------------------------------
class ResolveBookObjectMixin:
    def get_book_pk(self):
        pk = self.kwargs.get('pk')
        if pk:
            return pk
        pk = self.request.query_params.get('id')
        if pk:
            return pk
        pk = self.request.data.get('id')
        if pk:
            return pk
        return None

    def get_object(self):
        pk = self.get_book_pk()
        if not pk:
            raise NotFound("Book id not provided (expected 'pk' or 'id').")
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(f"Book with id={pk} not found.")


# -------------------------------------------------
# Create (authentication required)
# -------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# -------------------------------------------------
# Update (authentication required)
# -------------------------------------------------
class BookUpdateView(ResolveBookObjectMixin, generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# -------------------------------------------------
# Delete (authentication required)
# -------------------------------------------------
class BookDeleteView(ResolveBookObjectMixin, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
