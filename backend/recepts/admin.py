from django.contrib import admin
from django.core.exceptions import ValidationError

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

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions.get('ingredients') == None:
            raise ValidationError(
                'Список ингридиентов пуст'
            )
        return actions

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
