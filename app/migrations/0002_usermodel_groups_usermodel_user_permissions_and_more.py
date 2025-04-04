# Generated by Django 5.1.7 on 2025-04-04 19:32

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='date_joined',
            field=models.DateTimeField(db_column='date_joined', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='phone',
            field=models.CharField(db_column='phone_number', max_length=9, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number with country code (e.g., 123456789).', regex='^\\d{9}$')]),
        ),
        migrations.CreateModel(
            name='RaportsLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raport_link1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raport_link1', to='app.raports')),
                ('raport_link2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raport_link2', to='app.raports')),
            ],
            options={
                'verbose_name': 'Raport_Linked',
                'verbose_name_plural': 'Raports_Linked',
            },
        ),
    ]
