# Generated by Django 4.1 on 2024-07-06 03:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("social_media_app", "0002_alter_user_table"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="User",
            new_name="Account",
        ),
        migrations.AlterModelTable(
            name="account",
            table="account",
        ),
    ]
