# Generated by Django 5.1.3 on 2024-12-10 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='banners/')),
                ('alt_text', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Banners',
            },
        ),
    ]
