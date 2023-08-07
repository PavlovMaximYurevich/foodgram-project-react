from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'

    ALL_ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        'Никнейм',
        max_length=150,
        help_text='Введите ник пользователя',
        unique=True
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        help_text='Введите имя пользователя',
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        help_text='Введите фамилию пользователя',
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        help_text='Пароль',
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=50,
        choices=ALL_ROLES,
        default=USER
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_user'
            )
        ]

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя')
        # super(Follow, self).clean()
