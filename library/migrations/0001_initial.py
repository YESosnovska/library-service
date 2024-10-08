# Generated by Django 5.1.1 on 2024-09-14 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                (
                    "cover",
                    models.CharField(
                        choices=[("Hard", "Hard"), ("Soft", "Soft")], max_length=10
                    ),
                ),
                ("inventory", models.PositiveIntegerField(default=0)),
                (
                    "daily_fee",
                    models.DecimalField(decimal_places=2, default=0, max_digits=5),
                ),
            ],
        ),
    ]
