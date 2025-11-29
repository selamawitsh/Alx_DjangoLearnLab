# api/test_views.py

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .models import Book, Author


class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        self.author = Author.objects.create(name="Test Author")

        self.book1 = Book.objects.create(title="Alpha", publication_year=2001, author=self.author)
        self.book2 = Book.objects.create(title="Beta", publication_year=1999, author=self.author)

        self.client = APIClient()

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Alpha")
        self.assertEqual(response.data["author"], self.author.id)

    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        data = {"title": "New Book", "publication_year": 2024, "author": self.author.id}

        unauth = self.client.post(url, data, format="json")
        self.assertIn(unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(self.user)
        auth = self.client.post(url, data, format="json")
        self.assertEqual(auth.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        url = reverse("book-update-with-pk", kwargs={"pk": self.book1.id})
        data = {"title": "Updated Alpha", "publication_year": 2005, "author": self.author.id}

        unauth = self.client.put(url, data, format="json")
        self.assertIn(unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(self.user)
        auth = self.client.put(url, data, format="json")
        self.assertEqual(auth.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Alpha")

    def test_delete_book(self):
        url = reverse("book-delete-with-pk", kwargs={"pk": self.book2.id})

        unauth = self.client.delete(url)
        self.assertIn(unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(self.user)
        auth = self.client.delete(url)
        self.assertEqual(auth.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_filter_books(self):
        url = reverse("book-list") + "?publication_year=1999"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Beta")

    def test_search_books(self):
        url = reverse("book-list") + "?search=Alpha"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Alpha")

    def test_order_books(self):
        url = reverse("book-list") + "?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Beta")
        self.assertEqual(response.data[1]["title"], "Alpha")
