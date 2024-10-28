from django.contrib.auth.models import User
from django.db import models


class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='profile')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='фото', default='default.webp')
    birthdate = models.DateField(blank=True, null=True, verbose_name='дата рождения')
    data_joined = models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')
    points = models.IntegerField(default=0, verbose_name='количество баллов')
    role = models.CharField(max_length=100, choices=[('user', 'Пользователь'), ('admin', 'Администратор')],
                            verbose_name='роль на сайте')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'main_profiles'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['-data_joined', 'id']

    @property
    def age(self):
        from datetime import date
        if self.birthdate:
            today = date.today()
            return today.year - self.birthdate.year - (
                    (today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return None
