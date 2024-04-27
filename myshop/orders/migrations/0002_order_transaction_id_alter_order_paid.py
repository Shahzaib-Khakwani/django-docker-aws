# Generated by Django 4.1 on 2024-04-27 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="transaction_id",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="paid",
            field=models.BooleanField(default=False),
        ),
    ]