from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models

from recepts.models import (Favourites,
                            IngridientAmount,
                            Ingredients,
                            Recept,
                            ShoppingList,
                            Tag,
                            )


class IngredientsInReceptAdmin(admin.TabularInline):
    model = IngridientAmount
    min_num = 1
    # can_delete = False

    # def has_delete_permission(self, request, obj=None):
    #     if not self.model.ingredient:
    #         return False
    #     return True
    # def clean(self):
    #     ingr = Ingredients.objects.all()
    #     if len(ingr) < 1:
    #         raise ValidationError(
    #             'Нет ингридиентов'
    #         )
    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions.get("ingredients") is None:
            raise ValidationError(
                "Нет ингридиентов"
            )


class ReceptAdmin(admin.ModelAdmin):
    inlines = (IngredientsInReceptAdmin, )
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time'
    )

    search_fields = ('name', 'author')
    list_filter = ('name', 'author')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name', )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    search_fields = ('name', )


class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recept')
    search_fields = ('user', 'recept')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recept')
    search_fields = ('user', 'recept')


class IngridientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recept',
        'amount'
    )


admin.site.register(Recept, ReceptAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favourites, FavouritesAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(IngridientAmount, IngridientAmountAdmin)
