from django.db import models

from users.models import User

# CHECK_COLOR = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
CHECK_SLUG = r'^[-a-zA-Z0-9_]+$'


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
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='Ингридиенты',
        help_text='Выберите ингридиенты для рецепта'
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
    )
    time_cooking = models.PositiveIntegerField(
        'Время приготовления в минутах',
        help_text='Укажите время приготовления в минутах'
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name_recept


class Favourites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name='favourite',
        verbose_name='Пользователь'
    )
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
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
        return f'У пользователя {self.user} есть свой рецепт - {self.recept}'
