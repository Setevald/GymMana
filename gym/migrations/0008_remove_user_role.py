# Generated by Django 5.1.3 on 2024-12-11 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0007_user_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
