from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    It automatically includes all fields defined in the Book model.
    """
    class Meta:
        model = Book
        fields = '__all__' # Includes 'id', 'title', and 'author'