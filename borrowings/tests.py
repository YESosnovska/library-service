import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingDetailSerializer,
    BorrowingSerializer,
)
from library.models import Book

BORROWING_URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


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


class UnauthenticatedBorrowingApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(user=self.user)

    def test_borrowing_list(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_borrowing(self):
        book = sample_book()
        payload = {
            "expected_return_date": datetime.date.today(),
            "book": book.id,
        }

        res = self.client.post(BORROWING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_borrowing_detail(self):
        book = sample_book()
        borrowing = Borrowing.objects.create(
            expected_return_date=datetime.date.today(), book=book, user=self.user
        )

        url = detail_url(book.id)

        res = self.client.get(url)

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminBorrowingApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_borrowing_list_filtering(self):
        book = sample_book()
        borrowing = Borrowing.objects.create(
            expected_return_date=datetime.date.today(), book=book, user=self.user
        )

        user_2 = get_user_model().objects.create_user(
            email="test2@test.com",
            password="password",
        )
        borrowing_2 = Borrowing.objects.create(
            expected_return_date=datetime.date.today(), book=book, user=user_2
        )

        res = self.client.get(BORROWING_URL, {"user_id": user_2.id})

        borrowing_serializer = BorrowingSerializer(borrowing)
        borrowing_2_serializer = BorrowingSerializer(borrowing_2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(borrowing_2_serializer.data, res.data)
        self.assertNotIn(borrowing_serializer.data, res.data)
