from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'Название тэга',
        max_length=200,
        blank=False,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный идентификатор тэга',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        'Название ингридиента',
        blank=False,
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        blank=False,
        max_length=200
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recept(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recepts',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        help_text='Придумайте название рецепта'
    )
    image = models.ImageField(
        verbose_name='Фото рецепта',
        upload_to='recepts/',
    )
    text = models.TextField(
        'Подробное описание рецепта',
        help_text='Опишите детально рецепт'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='Ингридиенты',
        help_text='Выберите ингридиенты для рецепта',
        related_name='recepts',
        through='IngridientAmount'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах',
        help_text='Укажите время приготовления в минутах'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class Favourites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='Пользователь'
    )
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное',
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recept'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return (
            f'У пользователя {self.user} рецепт в избранном- {self.recept}'
        )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_shopper',
    )
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        related_name='user_shopper',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок',
        verbose_name_plural = 'Списки покупок',
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recept'],
                name='unique_shopping_list'
            )
        ]


class IngridientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        verbose_name='Ингридиент',
        on_delete=models.CASCADE
    )
    recept = models.ForeignKey(
        Recept,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1, message='количество должно быть положительным числом'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингридиент в рецепте',
        verbose_name_plural = 'Ингридиенты в рецепте',
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recept'],
                name='ingredient_in_recept'
            )
        ]
