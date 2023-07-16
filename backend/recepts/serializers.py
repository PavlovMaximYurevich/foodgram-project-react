from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from recepts.models import *
from users.serializers import *

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


class ReceptReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = SimpleUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recept
        fields = ("id",
                  "tags",
                  "author",
                  "ingredients",
                  "is_favorited",
                  "is_in_shopping_cart",
                  "name",
                  "image",
                  "text",
                  "cooking_time",
                  )

    def get_ingredients(self, obj):
        queryset = IngridientAmount.objects.filter(recept=obj)
        serializer = AllIngredientInReceptSerializer(
            queryset, many=True
        )
        return serializer.data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favourite.filter(recept=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.user_shopper.filter(recept=obj).exists()

