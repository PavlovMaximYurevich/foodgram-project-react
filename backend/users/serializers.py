import re
from datetime import datetime as dt
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from recepts.models import Recept
from .models import User, Follow

CHECK_USERNAME = r'^[\w.@+-]+'


class SimpleUserSerializer(UserSerializer):
    username = serializers.RegexField(
        CHECK_USERNAME,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'id',
                  # 'role',
                  # 'password',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and Follow.objects.filter(
            user=user.id, author=obj.id
        ).exists()


class SignupSerializer(UserCreateSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'id',
            'first_name',
            'last_name',
            'password',
        ]

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        nonunique_email = User.objects.filter(
            email=email).exclude(username=username).exists()
        nonunique_user = User.objects.filter(
            username=username).exclude(email=email).exists()
        if nonunique_user or nonunique_email:
            raise serializers.ValidationError(
                'Пользователь с такой почтой или именем уже существует!'
            )
        check_valid_username = re.search(
            CHECK_USERNAME,
            data.get('username'))
        if check_valid_username is None:
            raise ValidationError('Ошибка валидации')
        return data


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault())
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('id', 'user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author')
            )
        ]

    def validate(self, data):
        if data.get('user') == data.get('author'):
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!'
            )
        return data


class SubscriptionRead(serializers.ModelSerializer):

    class Meta:
        model = Recept
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
    # def to_internal_value(self, data):
    #     return data


class FollowReadSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )

    def get_recipes(self, obj):
        queryset = Recept.objects.filter(author=obj)
        if queryset:
            serializer = SubscriptionRead(
                queryset,
                context={'request': self.context.get('request')},
                many=True
            )
            return serializer.data

    def get_recipes_count(self, obj):
        queryset = Recept.objects.filter(author=obj).count()
        return queryset

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and Follow.objects.filter(
            user=user.id, author=obj.id
        ).exists()

    # def to_representation(self, instance):
    #     request = self.context.get('request')
    #     context = {'request': request}
    #     return SubscriptionRead(
    #         instance, context=context).data
    # def to_internal_value(self, data):
    #     return data
