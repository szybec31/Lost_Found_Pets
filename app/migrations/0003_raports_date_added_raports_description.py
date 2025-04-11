# Generated by Django 5.1.7 on 2025-04-11 12:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_usermodel_groups_usermodel_user_permissions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='raports',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='raports',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
    ]
