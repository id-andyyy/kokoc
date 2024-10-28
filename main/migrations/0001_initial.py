# Generated by Django 5.1.1 on 2024-10-12 19:36

import django.db.models.deletion
import imagekit.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tournament', models.CharField(max_length=255, verbose_name='турнир')),
                ('opponent', models.CharField(max_length=255, verbose_name='соперник')),
                ('date', models.DateField(verbose_name='дата матча')),
                ('time', models.TimeField(verbose_name='время начала матча')),
                ('description', models.TextField(blank=True, verbose_name='описание матча')),
                ('stadium', models.CharField(max_length=255, verbose_name='стадион')),
                ('link', models.URLField(blank=True, verbose_name='ссылка на матч')),
                ('stats', models.TextField(blank=True, verbose_name='статистика матча')),
            ],
            options={
                'verbose_name': 'матч',
                'verbose_name_plural': 'матчи',
                'db_table': 'main_matches',
                'ordering': ['-date', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='название экспоната')),
                ('description', models.TextField(verbose_name='описание')),
                ('date', models.DateField(verbose_name='дата')),
            ],
            options={
                'verbose_name': 'объект музея',
                'verbose_name_plural': 'объекты музея',
                'db_table': 'main_museum',
                'ordering': ['-date', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Representatives',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='имя представителя')),
                ('photo', models.ImageField(blank=True, upload_to='team_photos/%Y/%m/%d/', verbose_name='фото')),
                ('birthdate', models.DateField(verbose_name='дата рождения')),
                ('bio', models.TextField(blank=True, verbose_name='биография')),
                ('role', models.CharField(max_length=100, verbose_name='роль представителя')),
            ],
            options={
                'verbose_name': 'представитель',
                'verbose_name_plural': 'представители',
                'db_table': 'main_representatives',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='наименование товара')),
                ('photo1', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='shop_photos/', verbose_name='фото')),
                ('photo2', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='shop_photos/', verbose_name='фото')),
                ('photo3', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='shop_photos/', verbose_name='фото')),
                ('price', models.IntegerField(verbose_name='цента товара')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'товар магазина',
                'verbose_name_plural': 'товары магазина',
                'db_table': 'main_shop',
                'ordering': ['price', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='имя игрока')),
                ('photo', models.ImageField(blank=True, upload_to='team_photos/%Y/%m/%d/', verbose_name='фото')),
                ('birthdate', models.DateField(verbose_name='дата рождения')),
                ('bio', models.TextField(blank=True, verbose_name='биография')),
                ('position', models.CharField(max_length=100, verbose_name='позиция')),
                ('tshirt_number', models.IntegerField(default=0, verbose_name='номер игрока')),
                ('matches', models.IntegerField(default=0, verbose_name='матчи')),
                ('goals', models.IntegerField(default=0, verbose_name='голы')),
                ('red_cards', models.IntegerField(default=0, verbose_name='красные карточки')),
                ('yellow_cards', models.IntegerField(default=0, verbose_name='желтые карточки')),
                ('is_active', models.BooleanField(default=True, verbose_name='активен ли игрок')),
            ],
            options={
                'verbose_name': 'игрок',
                'verbose_name_plural': 'игроки',
                'db_table': 'main_team',
                'ordering': ['-is_active', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='заголовок')),
                ('content', models.TextField(verbose_name='контент')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='изменено')),
                ('likes', models.IntegerField(default=0, verbose_name='накрученные лайки')),
                ('legal_likes', models.TextField(blank=True, verbose_name='кто поставил легальный лайк')),
                ('count_likes', models.IntegerField(default=0)),
                ('count_comments', models.IntegerField(default=0)),
                ('photo', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='news_photos/%Y/%m/%d/', verbose_name='обложка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_news', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'статью',
                'verbose_name_plural': 'статьи',
                'db_table': 'main_articles',
                'ordering': ['-created_at', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='контент')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blank', models.TextField(blank=True, verbose_name='тест')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Комментарии', to='main.articles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='articles',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='article_comments', to='main.comment'),
        ),
    ]
