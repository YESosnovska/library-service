from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from library.models import Book
from library.serializers import BookSerializer

LIBRARY_URL = reverse("library:book-list")


def detail_url(book_id):
    return reverse("library:book-detail", args=[book_id])


def sample_book(**params) -> Book:
    defaults = {
        "title": "Test Book",
        "author": "test author",
        "cover": "Soft",
        "inventory": 15,
        "daily_fee": 1.50,
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


class UnauthenticatedLibraryApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        res = self.client.get(LIBRARY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedLibraryApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_book_details(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.get(url)

        serializer = BookSerializer(book)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_is_forbidden(self):
        load_data = {
            "title": "Test Book",
            "author": "test author",
            "cover": "Soft",
            "inventory": 15,
            "daily_fee": 1.5,
        }

        res = self.client.post(LIBRARY_URL, load_data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_is_forbidden(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_is_forbidden(self):
        book = sample_book()
        url = detail_url(book.id)
        load_data = {
            "title": "Test Book",
        }
        res = self.client.patch(url, load_data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedBookApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_book_is_allowed(self):
        load_data = {
            "title": "Test Book",
            "author": "test author",
            "cover": "Soft",
            "inventory": 15,
            "daily_fee": 1.5,
        }
        res = self.client.post(LIBRARY_URL, load_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete_book_is_allowed(self):
        book = sample_book()
        url = detail_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_book_is_allowed(self):
        book = sample_book()
        url = detail_url(book.id)
        load_data = {
            "title": "Test Book",
        }
        res = self.client.patch(url, load_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
