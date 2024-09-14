from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.select_related("user", "book")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        user = self.request.user

        if user.is_staff:
            return queryset

        return queryset.filter(user=user, actual_return_date__isnull=True)

    def perform_create(self, serializer):
        user = self.request.user
        active_borrowings = Borrowing.objects.filter(
            user=user, actual_return_date__isnull=True
        )

        if active_borrowings.exists():
            raise ValidationError(
                "You already have an active borrowing. Please return the current book before borrowing a new one."
            )
        book = serializer.validated_data["book"]
        if book.inventory <= 0:
            raise ValidationError("The book is currently out of stock.")

        book.inventory -= 1
        book.save()
        instance = serializer.save(user=user)
        return instance
