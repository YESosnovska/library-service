# Generated by Django 5.1.1 on 2024-09-14 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0006_alter_borrowing_book_id"),
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="book_id",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="book",
                to="library.book",
            ),
        ),
    ]
