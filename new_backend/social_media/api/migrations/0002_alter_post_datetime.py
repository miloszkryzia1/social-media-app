# Generated by Django 5.0.7 on 2024-07-18 22:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="datetime",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 18, 15, 26, 2, 760920)
            ),
        ),
    ]
