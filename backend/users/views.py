from models import User
from djoser.views import UserViewSet


class SimpleUserViewSet(UserViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated, IsAdminOnly,)
    # pagination_class = LimitOffsetPagination
    # filter_backends = (filters.SearchFilter,)
    # lookup_field = 'username'
    # search_fields = ('username',)
    # http_method_names = ('get', 'post', 'patch', 'delete')
    #
    # @action(
    #     methods=['get', 'patch'],
    #     detail=False,
    #     permission_classes=(IsAuthenticated,)
    # )
