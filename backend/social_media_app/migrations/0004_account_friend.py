# Generated by Django 4.1 on 2024-07-06 03:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social_media_app", "0003_rename_user_account_alter_account_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="friend",
            field=models.ManyToManyField(
                db_table="friendship", to="social_media_app.account"
            ),
        ),
    ]
