# Generated by Django 4.1 on 2024-02-24 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="cateogry",
            new_name="category",
        ),
    ]
