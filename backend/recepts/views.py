import csv

from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recepts.models import *
from recepts.serializers import *


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = pass


class IngridientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('name',)
    # permission_classes = pass


class ReceptViews(viewsets.ModelViewSet):
    queryset = Recept.objects.all()
    serializer_class = ReceptSerializer

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def favorite(self, request, pk):
        recept = get_object_or_404(Recept, pk=pk)
        user = self.request.user
        if self.request.method == 'POST':
            Favourites.objects.create(
                user=user,
                recept=recept
            )
            serializer = ReceptSerializer(recept)
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
    def shopping_card(self, request, pk):
        recept = get_object_or_404(Recept, pk=pk)
        user = request.user
        if self.request.method == 'POST':
            ShoppingList.objects.create(
                user=user,
                recept=recept
            )
            serializer = ReceptSerializer(recept)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE':
            shopping_list = get_object_or_404(
                ShoppingList, recept=recept, user=user
            )
            shopping_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_card(self, request):
        user = request.user
        ingredients = IngridientAmount.objects.filter(
            recept__user_shopper__user=user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="shopper.csv"'
            },
        )
        writer = csv.writer(response)
        writer.writerow(ingredients)
        for ingredient in list(ingredients):
            writer.writerow(ingredient)
        return response
