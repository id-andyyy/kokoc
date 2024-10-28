# Generated by Django 5.1.1 on 2024-10-10 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='default.webp', upload_to='photos/%Y/%m/%d/', verbose_name='фото')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='дата рождения')),
                ('data_joined', models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')),
                ('points', models.IntegerField(default=0, verbose_name='количество баллов')),
                ('role', models.CharField(choices=[('user', 'Пользователь'), ('admin', 'Администратор')], max_length=100, verbose_name='роль на сайте')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'db_table': 'main_profiles',
                'ordering': ['-data_joined', 'id'],
            },
        ),
    ]
