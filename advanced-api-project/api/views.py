# api/test_views.py

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .models import Book


class BookAPITests(APITestCase):

    def setUp(self):
        # Create user for authentication tests
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Example books
        self.book1 = Book.objects.create(title="Alpha", publication_year=2001)
        self.book2 = Book.objects.create(title="Beta", publication_year=1999)
        self.client = APIClient()

    # ---------------------------------------------------
    # TEST: LIST VIEW (read allowed for everyone)
    # ---------------------------------------------------
    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ---------------------------------------------------
    # TEST: DETAIL VIEW
    # ---------------------------------------------------
    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Alpha")

    # ---------------------------------------------------
    # TEST: CREATE REQUIRES AUTHENTICATION
    # ---------------------------------------------------
    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        data = {"title": "New Book", "publication_year": 2024}

        # Try unauthenticated → should fail
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticate and try again
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ---------------------------------------------------
    # TEST: UPDATE REQUIRES AUTHENTICATION
    # ---------------------------------------------------
    def test_update_book(self):
        url = reverse("book-update-with-pk", kwargs={"pk": self.book1.id})
        data = {"title": "Updated Alpha", "publication_year": 2005}

        # unauthenticated should fail
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticated request
        self.client.login(username="testuser", password="testpass123")
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Alpha")

    # ---------------------------------------------------
    # TEST: DELETE REQUIRES AUTHENTICATION
    # ---------------------------------------------------
    def test_delete_book(self):
        url = reverse("book-delete-with-pk", kwargs={"pk": self.book2.id})

        # unauthenticated should fail
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticated
        self.client.login(username="testuser", password="testpass123")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # ---------------------------------------------------
    # TEST: FILTERING
    # ---------------------------------------------------
    def test_filter_books(self):
        url = reverse("book-list") + "?publication_year=1999"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Beta")

    # ---------------------------------------------------
    # TEST: SEARCHING
    # ---------------------------------------------------
    def test_search_books(self):
        url = reverse("book-list") + "?search=Alpha"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Alpha")

    # ---------------------------------------------------
    # TEST: ORDERING
    # ---------------------------------------------------
    def test_order_books(self):
        url = reverse("book-list") + "?ordering=publication_year"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should be ordered by publication_year ascending: 1999, 2001
        self.assertEqual(response.data[0]["title"], "Beta")
        self.assertEqual(response.data[1]["title"], "Alpha")
