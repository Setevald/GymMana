# Generated by Django 5.1.3 on 2024-12-13 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0009_alter_classes_class_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='user',
            field=models.OneToOneField(default=100, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
