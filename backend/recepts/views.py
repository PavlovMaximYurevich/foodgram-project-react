from rest_framework import viewsets

from recepts.models import *
from recepts.serializers import *


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = pass


class IngridientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('name', )
    # permission_classes = pass