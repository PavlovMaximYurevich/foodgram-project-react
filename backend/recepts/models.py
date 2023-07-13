from django.db import models
from users.models import User


class Recept(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recepts',
        verbose_name='Автор рецепта'
    )
    name_recept = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        help_text='Придумайте название рецепта'
    )
    image = models.ImageField(
        verbose_name='Фото рецепта',
        upload_to='recepts/',
    )
    text_description = models.TextField(
        'Подробное описание рецепта',
        help_text='Опишите детально рецепт'
    )
    # ingredients = pass
    # tag = pass
    time_cooking = models.PositiveIntegerField(
        'Время приготовления в минутах',
        help_text='Укажите время приготовления в минутах'
    )
