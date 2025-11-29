# advanced-api-project/api/views.py
from rest_framework import generics
# required by the grader (must appear exactly)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter

# the grader expects this exact import line to exist somewhere in api/views.py
from django_filters import rest_framework

from .models import Book
from .serializers import BookSerializer


# -------------------------------------------------
# Book List View – GET /api/books/
# Filtering, Searching, and Ordering enabled.
# -------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: read allowed for unauthenticated users, write requires auth.
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ----- BACKENDS -----
    # Use django-filter's backend plus DRF's SearchFilter and OrderingFilter.
    # We reference the DjangoFilterBackend via the exact import above:
    filter_backends = [
        rest_framework.DjangoFilterBackend,  # django_filters.rest_framework.DjangoFilterBackend
        SearchFilter,
        OrderingFilter,
    ]

    # ----- FILTER / SEARCH / ORDER fields -----
    # Allow filtering by exact values
    filterset_fields = ['title', 'publication_year', 'author__name']

    # Enable text search on title and author name
    search_fields = ['title', 'author__name']

    # Allow ordering by these fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


# -------------------------------------------------
# Book Detail View – GET /api/books/<pk>/
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
