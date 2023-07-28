from django_filters import rest_framework as filters

from recepts.models import Tag, Recept, Ingredients


class ReceptFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recept
        fields = ('author', 'tags')

    def get_is_favorited(self, qs, value):
        if self.request.user.is_authenticated and value:
            return qs.filter(favourite__user=self.request.user)
        return qs

    def get_is_in_shopping_cart(self, qs, value):
        if self.request.user.is_authenticated and value:
            return qs.filter(user_shopper__user=self.request.user)
        return qs


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredients
        fields = ('name', )
