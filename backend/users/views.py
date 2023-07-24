from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import User, Follow
from .serializers import FollowSerializer, FollowReadSerializer
from djoser.views import UserViewSet


class SimpleUserViewSet(UserViewSet):
    # queryset = User.objects.all()
    # serializer_class = SimpleUserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    @action(
        methods=['get'],
        detail=False,
    )
    def subscriptions(self, request):
        user = request.user

        followers = User.objects.filter(following__user=user)
        # queryset = Follow.objects.filter(follower=user)
        print(followers)
        # print(queryset)
        pages = self.paginate_queryset(followers)
        print(pages)
        serializer = FollowReadSerializer(
            # pages,
            followers,
            # queryset,
            many=True,
            context={'request': request}
        )
        print(serializer.data)
        return self.get_paginated_response(serializer.data)
        # return serializer.data

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        id_author = self.kwargs.get('id')
        author = get_object_or_404(User, id=id_author)
        follower = get_object_or_404(Follow, user=user, author=author)
        if request.method == 'POST':
            serializer = FollowSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follower.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
