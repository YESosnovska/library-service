from rest_framework import serializers

from borrowings.models import Borrowing
from library.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book_id = serializers.CharField(source="book.book_id", read_only=True)
    user_id = serializers.CharField(source="user.user_id", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


class BorrowingListSerializer(serializers.ModelSerializer):
    book_id = serializers.CharField(source="book.book_id", read_only=True)
    user_id = serializers.CharField(source="user.user_id", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    user_id = serializers.CharField(source="user.user_id", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user_id",
        )
