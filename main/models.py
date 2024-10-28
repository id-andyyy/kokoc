from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', related_name='articles')
    title = models.CharField(max_length=255, verbose_name='заголовок')
    content = models.TextField(verbose_name='контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='изменено')
    likes = models.IntegerField(default=0, verbose_name='накрученные лайки')
    legal_likes = models.TextField(blank=True, verbose_name='кто поставил легальный лайк')
    count_likes = models.IntegerField(default=0)
    count_comments = models.IntegerField(default=0)
    photo = ProcessedImageField(
        upload_to='news_photos/%Y/%m/%d/',
        processors=[ResizeToFit(1600, 400)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        verbose_name='обложка'
    )
    liked_by = models.ManyToManyField(User, related_name='liked_news', blank=True)
    comments = models.ManyToManyField('Comment', related_name='article_comments', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'main_articles'
        verbose_name = 'статью'
        verbose_name_plural = 'статьи'
        ordering = ['-created_at', 'id']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='comments')
    news = models.ForeignKey(Articles, on_delete=models.CASCADE,
                             related_name='Комментарии')
    content = models.TextField(verbose_name='контент')
    created_at = models.DateTimeField(auto_now_add=True)
    blank = models.TextField(verbose_name='тест', blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"


class Matches(models.Model):
    id = models.AutoField(primary_key=True)
    tournament = models.CharField(max_length=255, verbose_name='турнир')
    opponent = models.CharField(max_length=255, verbose_name='соперник')
    date = models.DateField(verbose_name='дата матча')
    time = models.TimeField(verbose_name='время начала матча')
    logo1 = models.CharField(verbose_name='логотип противника', blank='true')
    description = models.TextField(blank=True, verbose_name='описание матча')
    stadium = models.CharField(max_length=255, verbose_name='стадион')
    link = models.URLField(blank=True, verbose_name='ссылка на матч')
    stats = models.CharField(blank=True, verbose_name='статистика матча')

    def __str__(self):
        return self.opponent

    class Meta:
        db_table = 'main_matches'
        verbose_name = 'матч'
        verbose_name_plural = 'матчи'
        ordering = ['-date', 'id']


class NextMatches(models.Model):
    id = models.AutoField(primary_key=True)
    tournament = models.CharField(max_length=255, verbose_name='турнир')
    opponent = models.CharField(max_length=255, verbose_name='соперник')
    date = models.DateField(verbose_name='дата матча')
    time = models.TimeField(verbose_name='время начала матча')
    logo1 = models.CharField(verbose_name='логотип противника', blank='true')
    description = models.TextField(blank=True, verbose_name='описание матча')
    stadium = models.CharField(max_length=255, verbose_name='стадион')
    link = models.URLField(blank=True, verbose_name='ссылка на матч')
    stats = models.CharField(blank=True, verbose_name='статистика матча')

    def __str__(self):
        return self.opponent

    class Meta:
        db_table = 'main_next_matches'
        verbose_name = 'не сыгранный матч'
        verbose_name_plural = 'не сыгранные матчи'
        ordering = ['-date', 'id']


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='имя игрока')
    photo = models.ImageField(upload_to='team_photos/%Y/%m/%d/', blank=True, verbose_name='фото')
    birthdate = models.DateField(verbose_name='дата рождения')
    bio = models.TextField(verbose_name='биография', blank=True)
    position = models.CharField(max_length=100, verbose_name='позиция')
    tshirt_number = models.IntegerField(verbose_name='номер игрока', default=0)
    matches = models.IntegerField(verbose_name='матчи', default=0)
    goals = models.IntegerField(verbose_name='голы', default=0)
    red_cards = models.IntegerField(verbose_name='красные карточки', default=0)
    yellow_cards = models.IntegerField(verbose_name='желтые карточки', default=0)
    is_active = models.BooleanField(default=True, verbose_name='активен ли игрок')

    def __str__(self):
        return self.name

    def calculate_age(self):
        birthdate = self.birthdate
        today = datetime.now()
        age = today.year - birthdate.year

        # Корректируем возраст, если день рождения в текущем году еще не наступил
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1

        return age

    class Meta:
        db_table = 'main_team'
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'
        ordering = ['-is_active', 'id']


class Representatives(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='имя представителя')
    photo = models.ImageField(upload_to='team_photos/%Y/%m/%d/', blank=True, verbose_name='фото')
    birthdate = models.DateField(verbose_name='дата рождения')
    bio = models.TextField(verbose_name='биография', blank=True)
    role = models.CharField(max_length=100, verbose_name='роль представителя')

    def __str__(self):
        return self.name

    def calculate_age(self):
        birthdate = self.birthdate
        today = datetime.now()
        age = today.year - birthdate.year

        # Корректируем возраст, если день рождения в текущем году еще не наступил
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1

        return age

    class Meta:
        db_table = 'main_representatives'
        verbose_name = 'представитель'
        verbose_name_plural = 'представители'
        ordering = ['id']


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='наименование товара')
    photo1 = ProcessedImageField(
        upload_to='shop_photos/',
        processors=[ResizeToFill(800, 800)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        verbose_name='фото'
    )
    photo2 = ProcessedImageField(
        upload_to='shop_photos/',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        verbose_name='фото'
    )
    photo3 = ProcessedImageField(
        upload_to='shop_photos/',
        processors=[ResizeToFit(800, 800)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        verbose_name='фото'
    )
    price = models.IntegerField(verbose_name='цента товара')
    description = models.TextField(verbose_name='описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'main_shop'
        verbose_name = 'товар магазина'
        verbose_name_plural = 'товары магазина'
        ordering = ['price', 'id']
