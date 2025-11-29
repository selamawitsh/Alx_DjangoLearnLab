from django.db import models

# -----------------------------
# Author model
# -----------------------------
class Author(models.Model):
    """
    Represents a book author.
    Each author can have multiple books (one-to-many relationship).
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -----------------------------
# Book model
# -----------------------------
class Book(models.Model):
    """
    Represents a book with a title, publication year, 
    and a foreign key linking it to an Author.
    """

    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()

    # Foreign key -> One author can have many books
    author = models.ForeignKey(
        Author, related_name='books', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
