# Generated by Django 4.1 on 2024-07-08 01:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("social_media_app", "0010_friendrequest"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="friendrequest",
            table="friend_request",
        ),
    ]
