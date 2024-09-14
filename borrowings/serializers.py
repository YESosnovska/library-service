from rest_framework import serializers

from borrowings.models import Borrowing
from library.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Borrowing
        fields = ["user", "book", "borrow_date", "expected_return_date"]

    def validate(self, attrs):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if Borrowing.objects.filter(
                user=user, actual_return_date__isnull=True
            ).exists():
                raise serializers.ValidationError(
                    "You already have an active borrowing."
                )
        return attrs
