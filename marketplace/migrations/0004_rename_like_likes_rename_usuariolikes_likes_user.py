# Generated by Django 4.1 on 2022-09-25 02:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0003_rename_vistar_postview'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='like',
            new_name='likes',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='usuariolikes',
            new_name='user',
        ),
    ]