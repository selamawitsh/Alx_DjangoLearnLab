from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# -------------------------------------------
# Book Serializer
# -------------------------------------------
class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model fields and validates
    that publication_year is not in the future.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


# -------------------------------------------
# Author Serializer (Nested BookSerializer)
# -------------------------------------------
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author model including nested books.
    Uses BookSerializer to display related books.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
