from django.core.exceptions import ValidationError
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowReadSerializer


class SimpleUserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    @action(
        methods=['get'],
        detail=False,
    )
    def subscriptions(self, request):
        user = request.user
        followers = User.objects.filter(following__user=user)
        results = self.paginate_queryset(followers)
        serializer = FollowReadSerializer(
            results,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if self.request.method == 'POST':
            if Follow.objects.filter(author=author, user=user).exists():
                raise ValidationError('уже подписан')
            Follow.objects.create(user=user, author=author)
            serializer = FollowReadSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follower = get_object_or_404(Follow, user=user, author=author)
            follower.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
