from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from .models import Book
from .serializers import BookSerializer

# -------------------------------------------------
# Book List View – GET /api/books/
# Anyone can view the list of books.
# -------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------------------------
# Book Detail View – GET /api/books/<pk>/
# Anyone can view a single book.
# -------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------------------------
# Helper mixin to resolve object by multiple sources:
# - URL kwarg 'pk' (preferred)
# - query parameter 'id'
# - request.data['id'] (for POST/PUT/PATCH)
# Raises NotFound if not present or object missing.
# -------------------------------------------------
class ResolveBookObjectMixin:
    def get_book_pk(self):
        # try URL kwarg first (e.g. /books/1/update/)
        pk = self.kwargs.get('pk')
        if pk:
            return pk

        # then query parameters: /books/update/?id=1
        pk = self.request.query_params.get('id')
        if pk:
            return pk

        # finally, check request data (useful for form submissions)
        pk = self.request.data.get('id')
        if pk:
            return pk

        return None

    def get_object(self):
        pk = self.get_book_pk()
        if not pk:
            raise NotFound(detail="Book id not provided (expected 'pk' in URL, or 'id' in query/body).")
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise NotFound(detail=f"Book with id={pk} not found.")


# -------------------------------------------------
# Book Create View – POST /api/books/create/
# Only authenticated users can create books.
# -------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Any custom creation logic goes here
        serializer.save()


# -------------------------------------------------
# Book Update View – supports:
# - PUT/PATCH /api/books/<pk>/update/
# - PUT/PATCH /api/books/update/?id=<pk>
# - PUT/PATCH /api/books/update/ (with JSON body containing "id": <pk>)
# Only authenticated users can update books.
# -------------------------------------------------
class BookUpdateView(ResolveBookObjectMixin, generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # get_object() is provided by ResolveBookObjectMixin


# -------------------------------------------------
# Book Delete View – supports:
# - DELETE /api/books/<pk>/delete/
# - DELETE /api/books/delete/?id=<pk>
# - DELETE /api/books/delete/ (with JSON body containing "id": <pk>)
# Only authenticated users can delete books.
# -------------------------------------------------
class BookDeleteView(ResolveBookObjectMixin, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # get_object() is provided by ResolveBookObjectMixin
