from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User

MAX_SYMBOLS = 20


class Tag(models.Model):
    name = models.CharField(
        'Название тэга',
        max_length=200,
        unique=True,
    )
    color = ColorField(
        'Цвет',
        unique=True,
        max_length=7,
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
        return self.name[:MAX_SYMBOLS]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.value = self.color.upper()
        return super(Tag, self).save(force_insert, force_update, using, update_fields)


class Ingredients(models.Model):
    name = models.CharField(
        'Название ингридиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
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
        return self.name[:MAX_SYMBOLS]


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
        help_text='Придумайте название рецепта'
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recepts/',
    )
    text = models.TextField(
        'Подробное описание рецепта',
        unique=True,
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
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.name[:MAX_SYMBOLS]


class AbstractModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True


class Favourites(AbstractModel):

    class Meta:
        default_related_name = 'favourite'
        verbose_name = 'Избранное',
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recept'],
                name='unique_favourites'
            )
        ]

    def __str__(self):
        return (
            f'У пользователя {self.user}'
            f' рецепт в избранном- {self.recept}'[:MAX_SYMBOLS]
        )


class ShoppingList(AbstractModel):

    class Meta:
        default_related_name = 'user_shopper'
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
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                1,
                message='количество должно быть положительным числом'
            ),
            MaxValueValidator(
                1000,
                message='Вы уверены, что вы съедите столько?'
            )
        )
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
