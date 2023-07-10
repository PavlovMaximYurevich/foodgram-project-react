from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'

    ALL_ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        help_text='Введите имя пользователя',
        unique=True
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
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
