# Generated by Django 4.0.4 on 2022-05-27 12:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_remove_likepost_user_likepost_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='liked',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
