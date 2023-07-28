from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from recepts.filters import IngredientsFilter, ReceptFilter
from recepts.models import (Ingredients,
                            Recept,
                            IngridientAmount,
                            Favourites,
                            ShoppingList,
                            Tag)
from recepts.serializers import (ReceptSerializer,
                                 TagSerializer,
                                 IngredientSerializer,
                                 ShoppingListSerializer,
                                 ReceptReadSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('name', )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientsFilter


class ReceptViews(viewsets.ModelViewSet):
    queryset = Recept.objects.all()
    serializer_class = ReceptSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReceptFilter

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def favorite(self, request, pk):
        recept = get_object_or_404(Recept, pk=pk)
        user = self.request.user
        if self.request.method == 'POST':
            if Favourites.objects.filter(recept=recept, user=user).exists():
                raise ValidationError('уже есть в списке')
            Favourites.objects.create(
                user=user,
                recept=recept
            )
            serializer = ShoppingListSerializer(
                recept, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            favorite_recept = get_object_or_404(
                Favourites, recept=recept, user=user
            )
            favorite_recept.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def shopping_cart(self, request, pk):
        recept = get_object_or_404(Recept, pk=pk)
        user = self.request.user
        if self.request.method == 'POST':
            if ShoppingList.objects.filter(recept=recept, user=user).exists():
                raise ValidationError('уже есть в списке')
            ShoppingList.objects.create(
                user=user,
                recept=recept
            )
            serializer = ShoppingListSerializer(
                recept, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            shopping_list = get_object_or_404(
                ShoppingList, recept=recept, user=user
            )
            shopping_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngridientAmount.objects.filter(
            recept__user_shopper__user=user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = ''
        result = [(i.values()) for i in ingredients]
        for items in result:
            for item in items:
                shopping_list += str(item) + ' '
            shopping_list += '\n'
        response = HttpResponse(
            shopping_list,
            content_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="shopper.csv"'
            },
        )
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReceptReadSerializer
        return ReceptSerializer
