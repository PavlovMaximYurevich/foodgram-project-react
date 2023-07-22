from drf_extra_fields.fields import Base64ImageField
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

    def to_internal_value(self, data):
        return data


class IngredientAmountReceptSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all()
    )

    # id = serializers.IntegerField()
    # amount = serializers.SerializerMethodField()

    class Meta:
        model = IngridientAmount
        fields = ('id', )

    def to_internal_value(self, data):
        return data


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


class ReceptSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountReceptSerializer(many=True)
    # ingredients = IngredientSerializer(many=True)
    # ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()
    author = SimpleUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    # tags = TagSerializer(many=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recept
        fields = (
            'id',
            'ingredients',
            'tags',
            'author',
            'image',
            'name',
            'text',
            'cooking_time',
            # 'is_favorited',
            # 'is_in_shopping_cart'
        )

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Не выбрано ни одного тэга'
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Тэги не уникальны!'
            )
        return tags

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Не выбрано ни одного ингридиента'
            )
        all_ingredients = [ingredient['id'] for ingredient in ingredients]
        if len(all_ingredients) != len(set(all_ingredients)):
            raise serializers.ValidationError(
                'Ингридиенты не уникальны!'
            )
        return ingredients

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context['request'].user
        recept = Recept.objects.create(author=author, **validated_data)
        recept.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredients, id=ingredient.get('id')
            )
            IngridientAmount.objects.create(
                ingredient=current_ingredient,
                recept=recept,
                amount=ingredient.get('amount')
            )
        return recept

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredients, id=ingredient.get('id')
            )
            IngridientAmount.objects.create(
                recept=instance,
                ingredient=current_ingredient,
                amount=ingredient.get('amount')
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ReceptReadSerializer(
            instance, context=context).data


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recept
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
