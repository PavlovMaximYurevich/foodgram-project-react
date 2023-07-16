from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from recepts.models import *

CHECK_COLOR = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
CHECK_SLUG = r'^[-a-zA-Z0-9_]+$'


class TagSerializer(serializers.ModelSerializer):
    color = serializers.RegexField(
        CHECK_COLOR,
        max_length=7,
    )
    slug = serializers.RegexField(
        CHECK_SLUG,
        max_length=200
    )

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class AllIngredientInReceptSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = IngridientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientAmountReceptSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngridientAmount
        fields = ('id', 'amount')
