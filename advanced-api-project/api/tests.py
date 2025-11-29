# api/test_views.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from .models import Book, Author


class BookAPITests(APITestCase):
    def setUp(self):
        # Create user for authentication tests
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create an author (Book requires an author FK)
        self.author = Author.objects.create(name="Test Author")

        # Example books (attach the author)
        self.book1 = Book.objects.create(title="Alpha", publication_year=2001, author=self.author)
        self.book2 = Book.objects.create(title="Beta", publication_year=1999, author=self.author)

        # API client
        self.client = APIClient()

    # ---------------------------------------------------
    # TEST: LIST VIEW (read allowed for everyone)
    # ---------------------------------------------------
    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response.data is a list of serialized books
        self.assertEqual(len(response.data), 2)

    # ---------------------------------------------------
    # TEST: DETAIL VIEW
    # ---------------------------------------------------
    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Alpha")
        self.assertEqual(response.data["author"], self.author.id)

    # ---------------------------------------------------
    # TEST: CREATE REQUIRES AUTH
    # ---------------------------------------------------
    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        data = {"title": "New Book", "publication_year": 2024, "author": self.author.id}

        # unauthenticated -> should be unauthorized (401) according to DRF default behavior
        unauth_resp = self.client.post(url, data, format="json")
        self.assertIn(unauth_resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Authenticate and try again using force_authenticate
        self.client.force_authenticate(user=self.user)
        auth_resp = self.client.post(url, data, format="json")
        self.assertEqual(auth_resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

        # logout
        self.client.force_authenticate(user=None)

    # ---------------------------------------------------
    # TEST: UPDATE REQUIRES AUTH
    # ---------------------------------------------------
    def test_update_book(self):
        url = reverse("book-update-with-pk", kwargs={"pk": self.book1.id})
        data = {"title": "Updated Alpha", "publication_year": 2005, "author": self.author.id}

        # unauthenticated should fail
        unauth_resp = self.client.put(url, data, format="json")
        self.assertIn(unauth_resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated
        self.client.force_authenticate(user=self.user)
        auth_resp = self.client.put(url, data, format="json")
        self.assertEqual(auth_resp.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Alpha")

        self.client.force_authenticate(user=None)

    # ---------------------------------------------------
    # TEST: DELETE REQUIRES AUTH
    # ---------------------------------------------------
    def test_delete_book(self):
        url = reverse("book-delete-with-pk", kwargs={"pk": self.book2.id})

        # unauthenticated should fail
        unauth_resp = self.client.delete(url)
        self.assertIn(unauth_resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated
        self.client.force_authenticate(user=self.user)
        auth_resp = self.client.delete(url)
        self.assertEqual(auth_resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

        self.client.force_authenticate(user=None)

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
