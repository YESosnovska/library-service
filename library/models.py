from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=10, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.title}, author: {self.author}, left: {self.inventory}"
